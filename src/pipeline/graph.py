import logging
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

from src.schemas.permission import FeaturePermissionResult
from src.schemas.group import FeatureGroupsResult
from src.models.llm_worker import LLMWorker
from src.pipeline.state import PipelineState
from src.pipeline.nodes import (
    create_global_semaphore, 
    preprocess_node, 
    functionality_node, 
    group_node, 
    group_aggregate_node, 
    permission_node, 
    permission_aggregate_node, 
    transform_permission_node,
)

logger = logging.getLogger(__name__)

def route_group_node(state: PipelineState, config: RunnableConfig) -> list[Send]:

    # Get the group list of configured LLMs from the config
    llm_group_list: list[LLMWorker] = config["configurable"].get("llm_group_list", [])
    model_names = [llm.config.model for llm in llm_group_list]
    
    # Get the number of features to process from the state
    num_features = state["feature_result"].number_of_features

    # Create Global Semaphore to limit the number of concurrent threads
    #create_global_semaphore(num_features)
    create_global_semaphore(3)

    sends = []
    
    # Cross product of model names and feature indices to create Send objects for each combination
    for model_name in model_names:
        for idx in range(num_features):

            featuregroupsresult = FeatureGroupsResult(
                tmp_model=model_name,
                tmp_feature_idx=idx,
                features=[]
            )

            sends.append(
                Send(
                    "group", 
                    {
                        **state,
                        "permission_groups_result": featuregroupsresult 
                    }
                )
            )

    logger.info(f"Analyzing groups using {len(sends)} instances across {len(model_names)} LLM models.")
    return sends

def route_permission_node(state: PipelineState, config: RunnableConfig) -> list[Send]:
    
    # Get the permission list of configured LLMs from the config
    llm_permission_list: list[LLMWorker] = config["configurable"].get("llm_permission_list", [])
    model_names = [llm.config.model for llm in llm_permission_list]
    
    # Get the features from the previous stage
    aggregate_result = state.get("feature_groups_aggregate_result")
    features_list = aggregate_result.features if aggregate_result else []
    
    # Set the Semaphore to the number of features to process
    #create_global_semaphore(len(features_list))
    create_global_semaphore(3)
    
    sends = []
    
    # For each model, for each feature, and for each group in the feature's inferences, create a llm call to analyze permissions.
    for model_name in model_names:
        for idx, feature in enumerate(features_list):
            for inference in feature.inferences:
                group_name = inference.group_name
                
                if group_name != "NONE":
                    permissionsresult = FeaturePermissionResult(
                        tmp_model=model_name,
                        tmp_feature_idx=idx,
                        tmp_group_name=group_name,
                        features=[]
                    )

                    sends.append(
                        Send(
                            "permission",
                            {
                                **state,
                                "permissions_result": permissionsresult 
                            }
                        )
                    )

    logger.info(f"Analyzing permissions using {len(sends)} instances across {len(model_names)} LLM models.")

    return sends


def build_app():
    # Initialize the StateGraph with the PipelineState schema
    workflow = StateGraph(PipelineState)

    # Nodes
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)
    workflow.add_node("group", group_node)
    workflow.add_node("group_arg", group_aggregate_node)
    workflow.add_node("permission", permission_node)
    workflow.add_node("permission_arg", permission_aggregate_node)
    workflow.add_node("transform_permission", transform_permission_node)
    

    # Edges
    workflow.add_edge(START, "preprocess")
    #workflow.add_edge("preprocess", END)
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("group", "group_arg")
    workflow.add_edge("permission", "permission_arg")
    workflow.add_edge("permission_arg", "transform_permission")
    workflow.add_edge("transform_permission", END)
    
    # Conditional edges
    workflow.add_conditional_edges(
        "function",
        route_group_node,
        {"group": "group"}
    )

    workflow.add_conditional_edges(
        "group_arg",
        route_permission_node,
        {"permission": "permission"}
    )

    return workflow.compile()