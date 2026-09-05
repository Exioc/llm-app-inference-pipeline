import logging
import threading
import json
import html2text
from typing import Dict, Any, List
from androguard.core.apk import APK
from langchain_core.runnables import RunnableConfig

from src.schemas.permission_data_types_mapping import PermissionDataTypeMapping, PermissionDataTypeMappingRegistry
# LABEL_TO_PERMISSIONS
from src.schemas.label_permission_mapping import AppPermission, ProcessedPermissions
from src.schemas.app_data import PermissionItem
from src.schemas.feature import FeatureResult
from src.pipeline.state import PipelineState
from src.utils.auto_save import auto_save
from src.utils.b64_decode import b64_decode
from src.utils.calculate_metrics import calculate_metrics
from src.utils.plot_metrics_summary import plot_metrics_summary
from src.utils.plot_permission_matrix import plot_permission_matrix
from src.prompts.feature_prompt import FEATURE_PROMPT
from src.prompts.group_prompt import GROUP_PROMPT
from src.prompts.permission_prompt import PERMISSION_PROMPT
from src.schemas.group import (
    FeatureGroupsResult,
    GroupInferenceAggregate,
    FeatureGroupsAggregate,
    FeatureGroupsAggregateResult
)
from src.schemas.permission import (
    FeaturePermissionAggregateResult,
    PermissionInferenceAggregate,
    FeaturePermissionAggregate,
    FeaturePermissionResult
)


logger = logging.getLogger(__name__)
global_semaphore = None

def create_global_semaphore(number: int):
    global global_semaphore
    global_semaphore = threading.Semaphore(number)


@auto_save("01_preprocessing")
def preprocess_node(state: PipelineState, config: RunnableConfig) -> dict:

    # Filteering option for apk permissions and ground truth 
    supported_apk_permissions = config["configurable"].get("supported_apk_permissions", False)
    supported_ground_truth_sets = config["configurable"].get("supported_ground_truth_sets", False)
    permissions_registry = config["configurable"].get("permissions_registry")

    metadata = state["metadata"]
    ground_truth_sets = state["ground_truth_sets"]

    # Base64 Decoding
    title = b64_decode(metadata.label)
    description = b64_decode(metadata.description.long)

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0  
    md_description = h.handle(description)

    # LABEL_TO_PERMISSIONS
    #===============================================================================================

    # permissions_mapping = config["configurable"].get("permissions_mapping", [])

    # # Get permissions labels from the metadata
    # permissions_labels: List[PermissionItem] = metadata.permissions
    
    # temp_permissions_map = {}
    
    # # Iterate over each permission category
    # for item in permissions_labels:
    #     category_name = item.category
        
    #     # if the category is not in the map, initialize it with an empty list
    #     if category_name not in temp_permissions_map:
    #         temp_permissions_map[category_name] = []
            
    #     # Iterate over each permission label in the category
    #     for label in item.permissions:
            
    #         # Check if the real permission name exists in the mapping
    #         if label in permissions_mapping.permissions:
    #             # Get the real android permission name from the mapping
    #             technical_name = permissions_mapping.permissions[label].name
    #         else:
    #             # Fallback, if the label is not found in the mapping
    #             technical_name = f"android.permission.UNKNOWN_{label.upper().replace(' ', '_')}"
            
    #         # Create an AppPermission instance and append it to the category list
    #         app_perm = AppPermission(
    #             name=technical_name,
    #             label=label
    #         )
    #         temp_permissions_map[category_name].append(app_perm)
            
    # # Wrap the final permissions map in a ProcessedPermissions instance
    # final_processed_permissions = ProcessedPermissions(permissions_map=temp_permissions_map)

    # ==============================================================================================

    apk_path = state["apk_path"]
    a = APK(apk_path)
    permissions = a.get_permissions()

    # Filter out permissions that do not start with "android.permission."
    apk_permissions = [perm.removeprefix('android.permission.') for perm in permissions if perm.startswith("android.permission.")]
    apk_permissions = [perm.replace(' ', '') for perm in apk_permissions if perm]
    number = len(apk_permissions)

    if supported_apk_permissions:
        apk_permissions = [perm for perm in apk_permissions if perm in permissions_registry.permissions]
        logger.info(f"Filtered APK permissions against the registry ({number - len(apk_permissions)} removed).")

    if supported_ground_truth_sets and ground_truth_sets:
        ground_truth_sets = [
            [perm for perm in sublist if perm in permissions_registry.permissions]
            for sublist in ground_truth_sets
        ]
        logger.info("Filtered permission sets against the registry of known permissions.")

    updates = {
        # LABEL_TO_PERMISSIONS
        #"permissions_map": final_processed_permissions.model_dump()["permissions_map"],
        "pkg": metadata.pkg,
        "label": title,
        "description_long": md_description,
        "apk_permissions": apk_permissions,
        "ground_truth_sets": ground_truth_sets,
        "metadata": None
    }

    logger.info("Preprocessing finished.")

    return updates
        
@auto_save("02_feature_extraction")
def feature_node(state: PipelineState, config: RunnableConfig) -> dict:

    # Get LLM
    llm_feature_list = config["configurable"].get("llm_feature_list", [])
    llm = llm_feature_list[0]

    messages = FEATURE_PROMPT.invoke({
        "label": state["label"],
        "description": state["description_long"]
    })

    try:
        llm_output = llm.run(messages)
    except Exception as e:
        logger.warning(f"First LLM call failed: {e}. Retrying once")
        try:
            llm_output = llm.run(messages)
        except Exception as e:
            logger.error(f"Second LLM call failed: {e}. Aborting.")
            raise

    number_of_features = len(llm_output.features) if llm_output.features else 0

    final_result = FeatureResult(
        inferred_by_model=llm.config.model,
        number_of_features=number_of_features,
        features=llm_output.features
    )
    
    logger.info(f"Feature extraction finished. Found {number_of_features} features.")

    return {
        "feature_result": final_result
    }

def group_router(state: PipelineState, config: RunnableConfig) -> dict:

    group_send_idx = state["group_send_idx"]
    group_send_idx += 1

    return {
        "group_send_idx": group_send_idx
    }


def group_node(state: dict[str, Any], config: RunnableConfig) -> dict:

    llm = state["llm"]
    feature = state["feature"]

    # Get the permission groups as JSON string for the prompt
    permission_groups = config["configurable"].get("permission_groups")
    context_string = permission_groups.model_dump_json(indent=2)
    
    # Prepare the prompt for the LLM
    messages = GROUP_PROMPT.invoke({
        "allowed_context": context_string,
        "label": feature.title,
        "description": feature.description
    })

    with global_semaphore:
        logger.info(f"Analyze feature '{feature.title}' using {llm.config.model}")
        # Make the LLM call to infer permission groups for the current feature
        try:
            result = llm.run(messages)
        except Exception as e:
            logger.warning(f"First LLM call failed: {e}. Retrying once")
            try:
                result = llm.run(messages)
            except Exception as e:
                logger.error(f"Second LLM call failed: {e}. Aborting.")
                raise

    # Save the result as a new entry in the state
    new_feature_entry = {
        "title": feature.title,       
        "description": feature.description,
        "inferred_by_model": llm.config.model,   
        "inferences": [item.model_dump() for item in result.inferences]
    }
    
    return {
        "feature_groups_result": FeatureGroupsResult(features=[new_feature_entry])
    }

@auto_save("03_group_arg")
def group_aggregate_node(state: PipelineState, config: RunnableConfig) -> dict:

    group_threshold = config["configurable"].get("group_threshold", 0.0)

    llm_group_list = config["configurable"].get("llm_group_list", [])
    number_of_models = len(llm_group_list)

    # Get data from the state
    raw_result = state.get("feature_groups_result")
    if not raw_result:
        return {"feature_groups_aggregate_result": FeatureGroupsAggregateResult(features=[])}
    
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


    if group_threshold > 0:

        aggregated_data_majority = {}

        for title, feature_data in aggregated_data.items():
            filtered_groups = {}
            
            for title, data in feature_data["groups_map"].items():
                value = len(data["models_inferred"]) / number_of_models
                if value >= group_threshold:
                    filtered_groups[title] = data

            if filtered_groups:
                aggregated_data_majority[title] = {
                    "title": feature_data["title"],
                    "description": feature_data["description"],
                    "groups_map": filtered_groups
                }
                
        aggregated_data = aggregated_data_majority


    # Convert the aggregated data into the final Pydantic target model
    final_features: List[FeatureGroupsAggregate] = []

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
            FeatureGroupsAggregate(
                title=data["title"],
                description=data["description"],
                inferences=container_inferences
            )
        )

    logger.info(f"Aggregation of all results from the group analysis with threshold {group_threshold}")

    return {
        "feature_groups_aggregate_result": FeatureGroupsAggregateResult(
            features=final_features,
            total_number_of_groups=total
        )
    }

def permission_router(state: PipelineState, config: RunnableConfig) -> dict:

    permission_send_idx = state["permission_send_idx"]
    permission_send_idx += 1

    return {
        "permission_send_idx": permission_send_idx
    }

def permission_node(state: dict[str, Any], config: RunnableConfig) -> dict:

    llm = state["llm"]
    group_name = state["group_name"]
    feature = state["feature"]

    # Get the permission groups as JSON string for the prompt
    all_permissions = config["configurable"].get("permissions")
    permission = next((perm for perm in all_permissions.groups if perm.group_name == group_name),None)
    if permission is None:
        logger.warning(f"No permission group found for {group_name}. Skipping permission analysis for this group.")
        return {
            "permissions_result": FeaturePermissionResult(features=[])
        }

    permissions_list = permission.model_dump()["permissions"]
    context_string = json.dumps(permissions_list, indent=2)

    # Prepare the prompt for the LLM
    messages = PERMISSION_PROMPT.invoke({
        "allowed_context": context_string,
        "group_name": group_name,
        "label": feature.title,
        "description": feature.description
    })

    with global_semaphore:
        logger.info(f"Analyze feature '{feature.title}' using group '{group_name}' and LLM model '{llm.config.model}")
        # Make the LLM call to infer permission groups for the current feature
        try:
            result = llm.run(messages)
        except Exception as e:
            logger.warning(f"First LLM call failed: {e}. Retrying once")
            try:
                result = llm.run(messages)
            except Exception as e:
                logger.error(f"Second LLM call failed: {e}. Aborting.")
                raise

    # Some llm models may return the permission name with the prefix "android.permission.", we need to remove it for consistency (qwen3.5:122B)
    for item in result.inferences:
        if item.permission_name:
            item.permission_name = item.permission_name.removeprefix("android.permission.")

    # Save the result as a new entry in the state
    new_feature_entry = {
        "title": feature.title,       
        "description": feature.description,
        "inferred_by_model": llm.config.model, 
        "group_name": group_name,  
        "inferences": [item.model_dump() for item in result.inferences]
    }
    
    return {
        "permissions_result": FeaturePermissionResult(features=[new_feature_entry])
    }

@auto_save("04_permission_arg")
def permission_aggregate_node(state: PipelineState, config: RunnableConfig) -> dict:

    permission_threshold = config["configurable"].get("permission_threshold", 0.0)

    llm_permission_list = config["configurable"].get("llm_permission_list", [])
    number_of_models = len(llm_permission_list)

    # Get data from the state
    raw_result = state.get("permissions_result")
    if not raw_result:
        return {"permission_aggregate_result": FeaturePermissionAggregateResult(features=[])}
    
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

    if permission_threshold > 0:
        aggregated_data_majority = {}

        for title, feature_data in aggregated_data.items():
            filtered_permissions = {}
            
            for title, data in feature_data["permissions_map"].items():
                value = len(data["models_inferred"]) / number_of_models
                if value >= permission_threshold:
                    filtered_permissions[title] = data

            if filtered_permissions:
                aggregated_data_majority[title] = {
                    "title": feature_data["title"],
                    "description": feature_data["description"],
                    "permissions_map": filtered_permissions
                }
                
        aggregated_data = aggregated_data_majority

    # Convert the aggregated data into the final Pydantic target model
    final_features: List[FeaturePermissionAggregate] = []

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
            FeaturePermissionAggregate(
                title=data["title"],
                description=data["description"],
                inferences=container_inferences
            )
        )

    logger.info(f"Aggregation of all results from the permission analysis with threshold {permission_threshold}")

    return {
        "feature_permission_aggregate_result": FeaturePermissionAggregateResult(
            features=final_features
        )
    }

# Extract the aggregated permission results into a clean list of predicted permissions
@auto_save("05_extract_permissions")
def extract_permissions_node(state: PipelineState, config: RunnableConfig) -> dict:
    feature_permission_aggregate_result = state.get("feature_permission_aggregate_result")
    features = feature_permission_aggregate_result.features if feature_permission_aggregate_result else []
    
    unique_permissions = set()
    for feature in features:
        for inference in feature.inferences:
            if inference.permission_name and inference.permission_name.strip().upper() != "NONE":    
                unique_permissions.add(inference.permission_name.strip().upper())
            
    return {
        "inferred_permissions": list(unique_permissions)
    }


@auto_save("06_validation")
def validation_node(state: PipelineState, config: RunnableConfig) -> dict:
    storage_path = state.get("storage_path")

    ground_truth_sets = state.get("ground_truth_sets", [])
    apk_permissions = state.get("apk_permissions", [])
    inferred_permissions = state.get("inferred_permissions", [])

    # -1 indicates that something went wrong while reading the variable.
    group_threshold = config["configurable"].get("group_threshold", -1)
    permission_threshold = config["configurable"].get("permission_threshold", -1)

    # get both permission sets if they exist, otherwise set them to empty lists
    permissions_set_1 = ground_truth_sets[0] if len(ground_truth_sets) > 0 else []
    permissions_set_2 = ground_truth_sets[1] if len(ground_truth_sets) > 1 else []

    # Convert all permission lists to sets for easier comparison and to remove duplicates
    permissions_set_1 = set(permissions_set_1)
    permissions_set_2 = set(permissions_set_2)
    apk_permissions = set(apk_permissions)
    inferred_permissions = set(inferred_permissions)

    # Calculate metrics and plot permission matrices for APK vs Pipeline
    apk_pipeline = calculate_metrics(apk_permissions, inferred_permissions, "APK", "Pipeline")
    plot_permission_matrix(
        ground_truth=apk_permissions,
        prediction= inferred_permissions,
        ground_truth_name='APK',
        prediction_name='Pipeline',
        output_dir=storage_path
    )

    # Collect metrics and sample data for plotting summary
    metrics_collection = {"apk_pipeline": apk_pipeline}
    sample_data = [apk_pipeline]

    # Calculate metrics and plot permission matrices for Set 1 vs Pipeline and APK vs Set 1 if Set 1 exists
    if permissions_set_1:
        set1_pipeline = calculate_metrics(permissions_set_1, inferred_permissions,"Set 1", "Pipeline")
        plot_permission_matrix(
            ground_truth=permissions_set_1,
            prediction= inferred_permissions,
            ground_truth_name='Set 1',
            prediction_name='Pipeline',
            output_dir=storage_path
        )

        # Apk as Ground Truth
        apk_set1 = calculate_metrics(apk_permissions, permissions_set_1, "APK", "Set 1")
        plot_permission_matrix(
            ground_truth=apk_permissions,
            prediction= permissions_set_1,
            ground_truth_name='APK',
            prediction_name='Set 1',
            output_dir=storage_path
        )

        # Collect metrics and sample data for plotting summary
        metrics_collection["set1_pipeline"] = set1_pipeline
        metrics_collection["apk_set1"] = apk_set1
        sample_data.append(set1_pipeline)
        sample_data.append(apk_set1)

    # Calculate metrics and plot permission matrices for Set 2 vs Pipeline and APK vs Set 2 if Set 2 exists
    if permissions_set_2:
        set2_pipeline = calculate_metrics(permissions_set_2, inferred_permissions, "Set 2", "Pipeline")
        plot_permission_matrix(
            ground_truth=permissions_set_2,
            prediction= inferred_permissions,
            ground_truth_name='Set 2',
            prediction_name='Pipeline',
            output_dir=storage_path
        )

        # Apk as Ground Truth
        apk_set2 = calculate_metrics(apk_permissions, permissions_set_2, "APK", "Set 2")
        plot_permission_matrix(
            ground_truth=apk_permissions,
            prediction= permissions_set_2,
            ground_truth_name='APK',
            prediction_name='Set 2',
            output_dir=storage_path
        )

        # Collect metrics and sample data for plotting summary
        metrics_collection["set2_pipeline"] = set2_pipeline
        metrics_collection["apk_set2"] = apk_set2
        sample_data.append(set2_pipeline)
        sample_data.append(apk_set2)


    # Plot the summary of all metrics
    plot_metrics_summary(metrics_list=sample_data,output_dir=storage_path)

    # Store the thresholds in State for metadata and reporting purposes
    threshold = {
        "group_threshold": group_threshold,
        "permission_threshold": permission_threshold
    }

    # # Convert to list because json.dumps cannot serialize sets
    set_collection = {
        "permissions_set_1": list(permissions_set_1),
        "permissions_set_2": list(permissions_set_2),
        "apk_permissions": list(apk_permissions),
        "inferred_permissions": list(inferred_permissions)
    }

    logger.info("Validation finished.")
    
    return {
        "metrics_collection" : metrics_collection,
        "threshold": threshold,
        "set_collection": set_collection
    }

@auto_save("07_data_types")
def data_types_node(state: PipelineState, config: RunnableConfig) -> dict:
    data_types_mapping = config["configurable"].get(
        "data_types_mapping", PermissionDataTypeMappingRegistry()
    )

    # Get all the permission sets from the state
    set_collection = state.get("set_collection", {})

    # Create a target dictionary to hold the permissions for which we want to find data types (APK and inferred permissions)
    target = {
        "inferred_permissions": set_collection.get("inferred_permissions", set()),
        "apk_permissions": set_collection.get("apk_permissions", set()),
    }

    # Create a lookup dictionary from the data types mapping for quick access
    lookup = data_types_mapping.as_dict

    # Iterate over the target permissions and map them to their corresponding data types
    result: dict[str, list[PermissionDataTypeMapping]] = {}
    for key, perms in target.items():
        mappings: list[PermissionDataTypeMapping] = []
        for perm in perms:
            perm_name = getattr(perm, "permission_name", perm) if not isinstance(perm, str) else perm
            data_types = lookup.get(perm_name, [])

            if not data_types:
                continue

            mappings.append(
                PermissionDataTypeMapping(
                    permission=perm_name,
                    data_types=data_types,
                )
            )

        result[key] = mappings

    logger.info("Data Type Mapping finished.")

    return {
        "data_types_collection": result
    }