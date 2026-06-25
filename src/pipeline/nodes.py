import logging
from typing import Dict, Any, List
from langchain_core.runnables import RunnableConfig

from src.pipeline.state import PipelineState
from src.utils.save_state import save_state
from src.utils.b64_decode import b64_decode
from src.prompts.func_prompt import FUNCTIONALITY_PROMPT
from src.prompts.group_prompt import GROUP_PROMPT
from src.models.llm import function_llm
from src.schemas.group_result import (
    PermissionGroupsResult,
    GroupInferenceAggregate,
    PermissionGroupsAggregateContainer,
    PermissionGroupsAggregateResult
)

logger = logging.getLogger(__name__)

def preprocess_node(state: PipelineState):
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
        "llmodel": state["llm_model"],
        "temperature": state["temperature"],
        "storage_path": state["storage_path"],
        "permissions_map": flattened_perms,
        "metadata": None
    }
    temp_state = {**state, **updates}
    save_state(temp_state, "01_preprocessing")

    logger.info("Preprocessing finished.")

    return updates
        

def functionality_node(state: PipelineState):
    messages = FUNCTIONALITY_PROMPT.invoke({
        "label": state["label"],
        "description": state["description_long"]
    })

    try:
        result = function_llm.invoke(messages)
    except Exception as e:
        # Use logger.error for failures. 
        logger.error(f"LLM invocation or parsing failed: {repr(e)}")
    
        try:
            if isinstance(e, OutputParserException) and hasattr(e, 'llm_output'):
                # Log the raw text that failed the parsing stage
                logger.error(f"Raw LLM output:\n{e.llm_output}")
        except Exception:
            pass
        raise
    
    number = len(result.features)

    temp_state = {
        **state, 
        **result.model_dump(),
        "number_of_features": number
    }
    save_state(temp_state, "02_functionality_extraction")

    logger.info(f"Feature extraction finished. Found {number} features.")

    return {
        "functionality_result": result,
        "number_of_features": number
    }

def group_node(state: PipelineState, config: RunnableConfig) -> dict:
    # Get the target model
    target_model_name = state["current_llm_model"]
    llm_group_list = config["configurable"].get("llm_group_list", [])
    chosen_llm = next((item for item in llm_group_list if item.model == target_model_name), None)
    group_llm = chosen_llm.instance 
    
    # Get the permission groups as JSON string for the prompt
    permission_groups = config["configurable"].get("permission_groups")
    context_string = permission_groups.model_dump_json(indent=2)
    
    # Get the target feature for this node
    feature_idx = state["current_feature_index"]
    current_feature = state["functionality_result"].features[feature_idx]
    
    # Prepare the prompt for the LLM
    messages = GROUP_PROMPT.invoke({
        "allowed_context": context_string,
        "label": current_feature.functionality,
        "description": current_feature.description
    })
    
    # Make the LLM call to infer permission groups for the current feature
    result = group_llm.invoke(messages)      
   
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

def aggregate_node(state: PipelineState) -> dict:
    logger.info("Group analysis finished across all instances.")
   
    # Get data from the state
    raw_result = state.get("group_permissions_result")
    if not raw_result:
        return {"permission_groups_aggregate_result": PermissionGroupsAggregateResult(features=[])}
    
    # Get features list from the raw result, handling both object and dict cases
    features_list = getattr(raw_result, "features", []) if hasattr(raw_result, "features") else raw_result.get("features", [])

    # Dict to hold aggregated data: {feature_title: {group_name: {reasoning, models_inferred}}}
    aggregated_data: Dict[str, Dict[str, Any]] = {}

    # Iterate over each feature container to aggregate group inferences
    for container in features_list:
        # Extract title, description, model name, and inferences, handling both Pydantic objects and dicts
        title = getattr(container, "title", None) or container.get("title")
        description = getattr(container, "description", None) or container.get("description")
        model_name = getattr(container, "inferred_by_model", None) or container.get("inferred_by_model")
        inferences = getattr(container, "inferences", []) or container.get("inferences", [])

        if not title:
            continue

        # Initialize the feature entry in the aggregated data if it doesn't exist
        if title not in aggregated_data:
            aggregated_data[title] = {
                "title": title,
                "description": description,
                "groups_map": {}
            }

        # Iterate over each inference to aggregate group names and reasoning
        for inf in inferences:
            if isinstance(inf, dict):
                g_name = inf.get("group_name")
                reasoning = inf.get("reasoning")
            else:
                g_name = getattr(inf, "group_name", None)
                reasoning = getattr(inf, "reasoning", None)

            if not g_name:
                continue

            # Remove spaces and convert to uppercase for normalization, if the llm model copy the group name directly
            normalized_g_name = g_name.replace(" ", "").upper()

            # if the group name is not already in the map for this feature, initialize it
            if normalized_g_name not in aggregated_data[title]["groups_map"]:
                aggregated_data[title]["groups_map"][normalized_g_name] = {
                    "group_name": normalized_g_name,
                    "reasoning": reasoning,
                    "models_inferred": []
                }

            # Add the llm model name to the list of models that inferred this group
            if model_name and model_name not in aggregated_data[title]["groups_map"][normalized_g_name]["models_inferred"]:
                aggregated_data[title]["groups_map"][normalized_g_name]["models_inferred"].append(model_name)

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

    state_update = {
        "permission_groups_aggregate_result": PermissionGroupsAggregateResult(features=final_features)
    }

    temp_state = {
        **state,
        **state_update
    }

    save_state(temp_state, "03_group_permission_arg")

    logger.info("Aggregation group node analysis finished across all instances.")

    return {
        "permission_groups_aggregate_result": PermissionGroupsAggregateResult(features=final_features)
    }