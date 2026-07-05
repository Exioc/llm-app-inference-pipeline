import argparse
import logging

from src.pipeline.graph import build_app
from src.utils.save_state import save_state
from src.utils.b64_decode import b64_decode
from src.utils.notify_me import notification
from src.utils.initialize_run_folder import initialize_run_folder
from src.utils.get_jsonl_line import get_jsonl_line
from src.utils.create_llm_pool import create_llm_pool
from src.schemas.app_data import AppMetadata
from src.config.config import (
    LANGSMITH_TRACING,
    load_permission_groups,
    load_permissions,
    setup_logging,
    llm_func_config,
    llm_group_config,
    llm_perm_config
)

logger = logging.getLogger(__name__)

def main() -> None:
    # Initialize logging
    setup_logging()

    # Create argument parser
    parser = argparse.ArgumentParser(description="Liest eine App-Metadaten-Zeile aus einer JSONL-Datei.")
    
    # Define required input arguments
    parser.add_argument("path", type=str, help="Pfad zur .jsonl Datei")
    parser.add_argument("index", type=int, help="Index der Zeile (beginnend bei 0)")

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract the specified line from the JSONL file
    app_data = get_jsonl_line(args.path, args.index)

    # Create a AppMetadata instance from the extracted data
    app_data = AppMetadata(**app_data)

    # Initialize run folder and save input
    storage_path = initialize_run_folder()
    save_state(app_data, "00_Metadata", storage_path)

    # Create LLM pool based on the configuration
    llm_func_list = create_llm_pool(llm_func_config)
    llm_group_list = create_llm_pool(llm_group_config)
    llm_perm_list = create_llm_pool(llm_perm_config)

    # Load permission groups and permissions
    permission_groups_model = load_permission_groups()
    permissions_model = load_permissions()

    # Build the pipeline
    app = build_app()

    # Input for the pipeline
    initial_input = {
        "metadata": app_data,
        "storage_path": storage_path
    }

    # Start the pipelin
    if LANGSMITH_TRACING == "true":
        logger.info("LangSmith tracing is active.")

    logger.info(f"Starting analysis pipeline for app: {b64_decode(initial_input['metadata'].label)}")

    final_state = app.invoke(
        initial_input,
        {
            "configurable": {
                "llm_func_list": llm_func_list,
                "llm_group_list": llm_group_list,
                "llm_perm_list": llm_perm_list,
                "permission_groups": permission_groups_model,
                "permissions": permissions_model,
                "group_filter": True,
                "permission_filter": True
            }
        },
    )

    logger.info("Analysis pipeline completed successfully.")
    notification.send()

if __name__ == "__main__":
    main()




