import logging
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

from src.schemas.group_result import PermissionGroupsResult
from src.models.llm_worker import LLMWorker
from src.pipeline.state import PipelineState
from src.pipeline.nodes import create_global_semaphore, preprocess_node, functionality_node, group_node, group_aggregate_node

logger = logging.getLogger(__name__)

def route_to_all_models_and_features(state: PipelineState, config: RunnableConfig) -> list[Send]:

    # Get the list of configured LLMs from the config
    llm_group_list: list[LLMWorker] = config["configurable"].get("llm_group_list", [])
    model_names = [llm.config.model for llm in llm_group_list]
    
    # Get the number of features to process from the state
    num_features = state["functionality_result"].number_of_features

    # Create Global Semaphore to limit the number of concurrent threads
    create_global_semaphore(num_features)
    
    sends = []
    
    # Cross product of model names and feature indices to create Send objects for each combination
    for model_name in model_names:
        for idx in range(num_features):

            permissiongroupsresult = PermissionGroupsResult(
                tmp_model=model_name,
                tmp_feature_idx=idx,
                features=state.get("features", []) 
            )

            sends.append(
                Send(
                    "group", 
                    {
                        **state,
                        "permission_groups_result": permissiongroupsresult 
                    }
                )
            )

    logger.info(f"Analyzing groups using {len(sends)} instances across {len(model_names)} LLM models.")
    return sends


def build_app():
    # Initialize the StateGraph with the PipelineState schema
    workflow = StateGraph(PipelineState)

    # Nodes
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)
    workflow.add_node("group", group_node)
    workflow.add_node("aggregate", group_aggregate_node)

    # Edges
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("group", "aggregate")
    workflow.add_edge("aggregate", END)
    
    # Conditional edges
    workflow.add_conditional_edges(
        "function",
        route_to_all_models_and_features,
        {"group": "group"}
    )

    return workflow.compile()