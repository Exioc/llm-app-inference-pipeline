import logging
import math 
import threading
import functools
from typing import Dict, Any, List
from langchain_core.runnables import RunnableConfig

from src.schemas.perm_map import AppPermission, ProcessedPermissions
from src.schemas.app_data import PermissionItem
from src.schemas.func_result import FunctionalityResult
from src.pipeline.state import PipelineState
from src.utils.save_state import save_state
from src.utils.b64_decode import b64_decode
from src.prompts.func_prompt import FUNCTIONALITY_PROMPT
from src.prompts.group_prompt import GROUP_PROMPT
from src.prompts.perm_prompt import PERM_PROMPT
from src.schemas.group_result import (
    PermissionGroupsResult,
    GroupInferenceAggregate,
    PermissionGroupsAggregateContainer,
    PermissionGroupsAggregateResult
)
from src.schemas.perm_result import (
    PermissionAggregateResult,
    PermissionInferenceAggregate,
    PermissionAggregateContainer,
    PermissionsResult
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
    title = b64_decode(metadata.label)
    description = b64_decode(metadata.description.long)

    # Flatten permissions: Category -> List of strings
    # flattened_perms = {
    #     item.category: item.permissions 
    #     for item in metadata.permissions
    # }

    permissions_mapping = config["configurable"].get("permissions_mapping", [])

    # 1. Hol die Raw-Daten aus dem State oder Input
    # (Laut deiner Definition eine Liste von PermissionItem-Objekten)
    raw_permissions: List[PermissionItem] = metadata.permissions
    
    # Hier legen wir das leere Dictionary an, das wir gleich befüllen
    temp_permissions_map = {}
    
    # 2. Durchlaufe jede Kategorie aus den Raw-Daten
    for item in raw_permissions:
        category_name = item.category
        
        # Falls die Kategorie noch nicht existiert, erstelle eine leere Liste
        if category_name not in temp_permissions_map:
            temp_permissions_map[category_name] = []
            
        # 3. Durchlaufe jedes Text-Label in dieser Kategorie
        for label in item.permissions:
            
            # 4. Abgleich mit deinem großen Mapping-Modell
            # (Ersetze 'permission_mapping' mit deiner globalen Variable/Instanz)
            if label in permissions_mapping.permissions:
                # Wenn das Label im Mapping existiert, holen wir uns den echten Namen
                technical_name = permissions_mapping.permissions[label].name
            else:
                # Fallback, falls Google mal ein neues Label einführt, das du noch nicht im Mapping hast
                technical_name = f"android.permission.UNKNOWN_{label.upper().replace(' ', '_')}"
            
            # 5. Erstelle das AppPermission-Objekt und füge es der Kategorie hinzu
            app_perm = AppPermission(
                name=technical_name,
                label=label
            )
            temp_permissions_map[category_name].append(app_perm)
            
    # 6. Verpacke das fertige Dictionary in dein ProcessedPermissions-Modell
    final_processed_permissions = ProcessedPermissions(permissions_map=temp_permissions_map)
    
    updates = {
        "pkg": metadata.pkg,
        "label": title,
        "description_long": description,
        "storage_path": state["storage_path"],
        "permissions_map": final_processed_permissions,
        "metadata": None
    }

    # updates = {
    #     "pkg": metadata.pkg,
    #     "label": label,
    #     "description_long": description,
    #     "storage_path": state["storage_path"],
    #     "permissions_map": flattened_perms,
    #     "permissions_map": final_processed_permission,
    #     "metadata": None
    # }

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

    # Get the target model
    target_model_name = state["permission_groups_result"].tmp_model
    llm_group_list = config["configurable"].get("llm_group_list", [])
    group_llm = next((item for item in llm_group_list if item.config.model == target_model_name), None)
    
    # Get the target feature for this node
    feature_idx = state["permission_groups_result"].tmp_feature_idx
    current_feature = state["functionality_result"].features[feature_idx]

    

    # Get the permission groups as JSON string for the prompt
    permission_groups = config["configurable"].get("permission_groups")
    context_string = permission_groups.model_dump_json(indent=2)
    
    # Prepare the prompt for the LLM
    messages = GROUP_PROMPT.invoke({
        "allowed_context": context_string,
        "label": current_feature.title,
        "description": current_feature.description
    })

    with global_semaphore:
        logger.info(f"Analyze feature {feature_idx+1} using {target_model_name}")

        # Make the LLM call to infer permission groups for the current feature
        result = group_llm.run(messages)

    # Save the result as a new entry in the state
    new_feature_entry = {
        "title": current_feature.title,       
        "description": current_feature.description,
        "inferred_by_model": target_model_name,   
        "inferences": [item.model_dump() for item in result.inferences]
    }
    
    return {
        "group_permissions_result": PermissionGroupsResult(features=[new_feature_entry])
    }

@auto_save("03_group_permission_arg")
def group_aggregate_node(state: PipelineState, config: RunnableConfig) -> dict:

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

            # Normalize group name by removing spaces and converting to uppercase because an LLM model copy the name with with spaces
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

        majority_threshold = math.ceil(number_of_models / 2)
        
        for title, feature_data in aggregated_data.items():
            filtered_groups = {}
            
            for g_name, g_data in feature_data["groups_map"].items():
                
                if len(g_data["models_inferred"]) >= majority_threshold:
                    filtered_groups[g_name] = g_data

            if filtered_groups:
                aggregated_data_majority[title] = {
                    "title": feature_data["title"],
                    "description": feature_data["description"],
                    "groups_map": filtered_groups
                }
                
        aggregated_data = aggregated_data_majority


    # Convert the aggregated data into the final Pydantic target model
    final_features: List[PermissionGroupsAggregateContainer] = []

    total = 0
    for title, data in aggregated_data.items():
        container_inferences: List[GroupInferenceAggregate] = []
        
        total += len(data["groups_map"]) 

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
        f"Aggregation of all results from the group analysis "
        f"(Majority filter active: {apply_filter})"
    )

    return {
        "functionality_result": None,
        "permission_groups_aggregate_result": PermissionGroupsAggregateResult(
            features=final_features,
            total_number_of_groups=total
        )
    }

def permission_node(state: PipelineState, config: RunnableConfig) -> dict:
 
    # Get the target model
    target_model_name = state["permissions_result"].tmp_model
    llm_perm_list = config["configurable"].get("llm_perm_list", [])
    perm_llm = next((item for item in llm_perm_list if item.config.model == target_model_name), None)
    
    # Get the target feature for this node
    feature_idx = state["permissions_result"].tmp_feature_idx
    current_feature = state["permission_groups_aggregate_result"].features[feature_idx]

    group_name = state["permissions_result"].tmp_group_name

    # Get the permission groups as JSON string for the prompt
    all_permissions = config["configurable"].get("permissions")
    permission = next((perm for perm in all_permissions.groups_details if perm.group_name == group_name),None)
    context_string = permission.model_dump_json(indent=2)
    
    # Prepare the prompt for the LLM
    messages = PERM_PROMPT.invoke({
        "allowed_context": context_string,
        "group_name": group_name,
        "label": current_feature.title,
        "description": current_feature.description
    })
    
    with global_semaphore:
        logger.info(f"Analyze feature {feature_idx+1} using the group {group_name} and the {target_model_name}")

        # Make the LLM call to infer permission groups for the current feature
        result = perm_llm.run(messages)

    # Save the result as a new entry in the state
    new_feature_entry = {
        "title": current_feature.title,       
        "description": current_feature.description,
        "inferred_by_model": target_model_name, 
        "group_name": group_name,  
        "inferences": [item.model_dump() for item in result.inferences]
    }
    
    return {
        "permissions_result": PermissionsResult(features=[new_feature_entry])
    }

@auto_save("04_permission_arg")
def permission_aggregate_node(state: PipelineState, config: RunnableConfig) -> dict:

    apply_filter = config["configurable"].get("permission_filter", False)

    llm_perm_list = config["configurable"].get("llm_perm_list", [])
    number_of_models = len(llm_perm_list)

    # Get data from the state
    raw_result = state.get("permissions_result")
    if not raw_result:
        return {"permission_aggregate_result": PermissionAggregateResult(features=[])}
    
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
            "permissions_map": {}
        })

        for inf in feature.inferences or []:
            if not inf.permission_name:
                continue

             # Normalize group name by removing spaces and converting to uppercase because an LLM model copy the name with with spaces
            normalized_p_name = inf.permission_name.replace(" ", "").upper()

            # Add permission entry if it doesn't exist
            permission_entry = feature_entry["permissions_map"].setdefault(normalized_p_name, {
                "permission_name": normalized_p_name,
                "reasoning": inf.reasoning,
                "models_inferred": []
            })

            # if the privious reasoning is empty and the current inference has reasoning, update it
            if inf.reasoning and not permission_entry["reasoning"]:
                permission_entry["reasoning"] = inf.reasoning

            # Add the model name to the list
            if feature.inferred_by_model and feature.inferred_by_model not in permission_entry["models_inferred"]:
                permission_entry["models_inferred"].append(feature.inferred_by_model)

    if apply_filter:
        aggregated_data_majority = {}

        majority_threshold = math.ceil(number_of_models / 2)
        
        for title, feature_data in aggregated_data.items():
            filtered_permissions = {}
            
            for p_name, p_data in feature_data["permissions_map"].items():
                if len(p_data["models_inferred"]) >= majority_threshold:
                    filtered_permissions[p_name] = p_data

            if filtered_permissions:
                aggregated_data_majority[title] = {
                    "title": feature_data["title"],
                    "description": feature_data["description"],
                    "permissions_map": filtered_permissions
                }
                
        aggregated_data = aggregated_data_majority

    # Convert the aggregated data into the final Pydantic target model
    final_features: List[PermissionAggregateContainer] = []

    for title, data in aggregated_data.items():
        container_inferences: List[PermissionInferenceAggregate] = []
        
        for norm_name, perm_data in data["permissions_map"].items():
            container_inferences.append(
                PermissionInferenceAggregate(
                    permission_name=perm_data["permission_name"],
                    reasoning=perm_data["reasoning"],
                    models_inferred=perm_data["models_inferred"]
                )
            )

        final_features.append(
            PermissionAggregateContainer(
                title=data["title"],
                description=data["description"],
                inferences=container_inferences
            )
        )

    logger.info(
        f"Aggregation of all results from the permission analysis "
        f"(Majority filter active: {apply_filter}"
    )

    return {
        "group_permissions_result": None,
        "permission_groups_aggregate_result": None,
        "permission_aggregate_result": PermissionAggregateResult(
            features=final_features
        )
    }