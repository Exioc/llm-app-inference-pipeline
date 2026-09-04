import argparse
import logging

from src.pipeline.nodes import create_global_semaphore
from src.pipeline.graph import build_app
from src.utils.save_state import save_state
from src.utils.b64_decode import b64_decode
from src.utils.notify_me import notification
from src.utils.initialize_run_folder import initialize_run_folder
from src.utils.get_jsonl_line import get_jsonl_line
from src.utils.create_llm_pool import create_llm_pool
from src.schemas.app_data import AppMetadata
from src.config.config import (
    # LABEL_TO_PERMISSIONS
    #load_permissions_mapping,
    LANGSMITH_TRACING,
    extract_permission_sets_from_md,
    load_data_types_mapping,
    load_permission_groups,
    load_permissions,
    load_permissions_registry,
    setup_logging,
    load_weights_config,
    llm_feature_config,
    llm_group_config,
    llm_permission_config
)

logger = logging.getLogger(__name__)

def main() -> None:
    # Initialize logging
    setup_logging()

    # Create argument parser
    parser = argparse.ArgumentParser(description="Reads an app metadata line from a JSONL file.")
    
    # Define required input arguments
    parser.add_argument("metadata_path", type=str, help="Path to the JSONL file containing app metadata.")
    parser.add_argument("index", type=int, help="Index of the line to read, start with 1.")
    parser.add_argument("apk_path", type=str, help="Path to the APK file.")
    parser.add_argument("ground_truth_path", type=str, help="Path to the ground truth file.", nargs="?")

    # Parse command-line arguments
    args = parser.parse_args()

    # Load ground truth permission sets if provided
    # ground_truth_sets is a list of lists, where each inner list contains a set of permissions.
    if args.ground_truth_path is not None:
        ground_truth_sets = extract_permission_sets_from_md(args.ground_truth_path)
    else:
        ground_truth_sets = []

    # Extract the specified line from the JSONL file
    app_data = get_jsonl_line(args.metadata_path, args.index)

    # Get the APK path from the command-line arguments
    apk_path = args.apk_path

    # Create a AppMetadata instance from the extracted data
    app_data = AppMetadata(**app_data)

    # Get name 
    app_name = b64_decode(app_data.label)

    # Initialize run folder and save input
    storage_path = initialize_run_folder(app_name)
    save_state(app_data, "00_Metadata", storage_path)

    # Create LLM pool based on the configuration
    llm_feature_list = create_llm_pool(llm_feature_config)
    llm_group_list = create_llm_pool(llm_group_config)
    llm_permission_list = create_llm_pool(llm_permission_config)

    thresholds = load_weights_config()

    # Load permission groups and permissions
    permission_groups = load_permission_groups()
    permissions = load_permissions()

    # LABEL_TO_PERMISSIONS
    # permissions_mapping = load_permissions_mapping()

    data_types_mapping = load_data_types_mapping()

    # Set to filter APK or other sets with permissions against the known permissions registry
    permissions_registry = load_permissions_registry()

    create_global_semaphore(1)

    # Build the pipeline
    app = build_app()

    # Input for the pipeline
    initial_input = {
        "metadata": app_data,
        "ground_truth_sets": ground_truth_sets,
        "storage_path": storage_path,
        "apk_path": apk_path,
        "group_send_idx": -1,
        "permission_send_idx": -1
    }

    # Start the pipelin
    if LANGSMITH_TRACING == "true":
        logger.info("LangSmith tracing is active.")

    logger.info(f"Starting analysis pipeline for app: {b64_decode(initial_input['metadata'].label)}")

    final_state = app.invoke(
        initial_input,
        {
            "configurable": {
                # LABEL_TO_PERMISSIONS
                #"permissions_mapping": permissions_mapping,
                "llm_feature_list": llm_feature_list,
                "llm_group_list": llm_group_list,
                "llm_permission_list": llm_permission_list,
                "permission_groups": permission_groups,
                "permissions": permissions,
                "permissions_registry": permissions_registry,
                "data_types_mapping": data_types_mapping,
                "group_threshold": thresholds.get("group", 0.0),
                "permission_threshold": thresholds.get("permission", 0.0),
                "supported_apk_permissions": True,
                "supported_ground_truth_sets": True
            }
        },
    )

    logger.info("Analysis pipeline completed successfully.")
    notification.send()

if __name__ == "__main__":
    main()




