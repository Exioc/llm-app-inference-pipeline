import logging
import math 
import threading
import functools
from typing import Dict, Any, List
from langchain_core.runnables import RunnableConfig

from src.schemas.func_result import FunctionalityResult
from src.pipeline.state import PipelineState
from src.utils.save_state import save_state
from src.utils.b64_decode import b64_decode
from src.prompts.func_prompt import FUNCTIONALITY_PROMPT
from src.prompts.group_prompt import GROUP_PROMPT
from src.schemas.group_result import (
    PermissionGroupsResult,
    GroupInferenceAggregate,
    PermissionGroupsAggregateContainer,
    PermissionGroupsAggregateResult
)

logger = logging.getLogger(__name__)
global_semaphore = None

def auto_save(step_name: str):
    def decorator(node_func):
        @functools.wraps(node_func)
        def wrapper(state, config, *args, **kwargs):
            # Execute the real node 
            result = node_func(state, config, *args, **kwargs)
            
            # Merge the result into the state
            temp_state = {**state, **result}
            
            # Save the state after the node execution
            save_state(temp_state, step_name)
            
            # Return the real result of the node
            return result
        return wrapper
    return decorator


def create_global_semaphore(number: int):
    
    global global_semaphore
    
    global_semaphore = threading.Semaphore(number)


@auto_save("01_preprocessing")
def preprocess_node(state: PipelineState, config=None) -> dict:
    metadata = state["metadata"]

    # Base64 Decoding
    label = b64_decode(metadata.label)
    description = b64_decode(metadata.description.long)

    # Flatten permissions: Category -> List of strings
    flattened_perms = {
        item.category: item.permissions 
        for item in metadata.permissions
    }

    updates = {
        "pkg": metadata.pkg,
        "label": label,
        "description_long": description,
        "storage_path": state["storage_path"],
        "permissions_map": flattened_perms,
        "metadata": None
    }

    logger.info("Preprocessing finished.")

    return updates
        
@auto_save("02_functionality_extraction")
def functionality_node(state: PipelineState, config: RunnableConfig) -> dict:

    # Get LLM
    llm_group_list = config["configurable"].get("llm_func_list", [])
    llm = llm_group_list[0]

    messages = FUNCTIONALITY_PROMPT.invoke({
        "label": state["label"],
        "description": state["description_long"]
    })

    llm_output = llm.run(messages)

    number_of_features = len(llm_output.features) if llm_output.features else 0

    final_result = FunctionalityResult(
        inferred_by_model=llm.config.model,
        number_of_features=number_of_features,
        features=llm_output.features
    )
    
    logger.info(f"Feature extraction finished. Found {number_of_features} features.")

    return {
        "functionality_result": final_result
    }

def group_node(state: PipelineState, config: RunnableConfig) -> dict:

    with global_semaphore:
        
        # Get the target model
        target_model_name = state["permission_groups_result"].tmp_model
        llm_group_list = config["configurable"].get("llm_group_list", [])
        group_llm = next((item for item in llm_group_list if item.config.model == target_model_name), None)
        
        # Get the target feature for this node
        feature_idx = state["permission_groups_result"].tmp_feature_idx
        current_feature = state["functionality_result"].features[feature_idx]

        logger.info(f"Model_name:{target_model_name} | Feature:{feature_idx+1}")

        # Get the permission groups as JSON string for the prompt
        permission_groups = config["configurable"].get("permission_groups")
        context_string = permission_groups.model_dump_json(indent=2)
        
        # Prepare the prompt for the LLM
        messages = GROUP_PROMPT.invoke({
            "allowed_context": context_string,
            "label": current_feature.functionality,
            "description": current_feature.description
        })
        
        # Make the LLM call to infer permission groups for the current feature
        result = group_llm.run(messages)

        # Save the result as a new entry in the state
        new_feature_entry = {
            "title": current_feature.functionality,       
            "description": current_feature.description,
            "inferred_by_model": target_model_name,   
            "inferences": [item.model_dump() for item in result.inferences]
        }
    
    return {
        "group_permissions_result": PermissionGroupsResult(features=[new_feature_entry])
    }

@auto_save("03_group_permission_arg")
def group_aggregate_node(state: PipelineState, config: RunnableConfig) -> dict:
    logger.info("Group analysis finished across all instances.")

    apply_filter = config["configurable"].get("group_filter", False)

    llm_group_list = config["configurable"].get("llm_group_list", [])
    number_of_models = len(llm_group_list)

    # Get data from the state
    raw_result = state.get("group_permissions_result")
    if not raw_result:
        return {"permission_groups_aggregate_result": PermissionGroupsAggregateResult(features=[])}
    
    # Get features list from the raw result
    features_list = getattr(raw_result, "features", [])

    # Dict to hold aggregated data: {feature_title: {group_name: {reasoning, models_inferred}}}
    aggregated_data: Dict[str, Dict[str, Any]] = {}

    # Iterate over each feature container to aggregate group inferences
    for feature in features_list:
        if not feature.title:
            continue

        # Add Feature entry if it doesn't exist
        feature_entry = aggregated_data.setdefault(feature.title, {
            "title": feature.title,
            "description": feature.description,
            "groups_map": {}
        })

        for inf in feature.inferences or []:
            if not inf.group_name:
                continue

            # Normalize group name by removing spaces and converting to uppercase becaause an LLM model copy the name with with spaces
            normalized_g_name = inf.group_name.replace(" ", "").upper()

            # Add group entry if it doesn't exist
            group_entry = feature_entry["groups_map"].setdefault(normalized_g_name, {
                "group_name": normalized_g_name,
                "reasoning": inf.reasoning,
                "models_inferred": []
            })

            # Add the model name to the list
            if feature.inferred_by_model and feature.inferred_by_model not in group_entry["models_inferred"]:
                group_entry["models_inferred"].append(feature.inferred_by_model)


    if apply_filter:

        aggregated_data_majority = {}
        
        for title, feature_data in aggregated_data.items():
            # Ein neues, leeres Körbchen für die Gruppen, die den Vote bestehen
            filtered_groups = {}
            
            # 1. FEHLER BEHOBEN: Wir iterieren direkt über die groups_map
            for g_name, g_data in feature_data["groups_map"].items():
                
                # Berechnung der Mehrheit (g_data ist jetzt garantiert ein Dict)
                if len(g_data["models_inferred"]) >= math.ceil(number_of_models / 2):
                    filtered_groups[g_name] = g_data

            # 2. LOGIK-FEHLER BEHOBEN: Nur wenn das Feature danach noch 
            # gültige Gruppen besitzt, übernehmen wir es in das Endergebnis
            if filtered_groups:
                aggregated_data_majority[title] = {
                    "title": feature_data["title"],
                    "description": feature_data["description"],
                    "groups_map": filtered_groups
                }
                
        aggregated_data = aggregated_data_majority


    # Now convert the aggregated data into the final output format
    final_features: List[PermissionGroupsAggregateContainer] = []

    for title, data in aggregated_data.items():
        container_inferences: List[GroupInferenceAggregate] = []
        
        for norm_name, group_data in data["groups_map"].items():
            container_inferences.append(
                GroupInferenceAggregate(
                    group_name=group_data["group_name"],
                    reasoning=group_data["reasoning"],
                    models_inferred=group_data["models_inferred"]
                )
            )

        final_features.append(
            PermissionGroupsAggregateContainer(
                title=data["title"],
                description=data["description"],
                inferences=container_inferences
            )
        )

    logger.info(
        f"Aggregation group node analysis finished across all instances. "
        f"(Majority filter active: {apply_filter})"
    )

    return {
        "permission_groups_aggregate_result": PermissionGroupsAggregateResult(features=final_features)
    }