import logging
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

from src.models.llm_worker import LLMWorker
from src.pipeline.state import PipelineState
from src.pipeline.nodes import (
    data_types_node, 
    preprocess_node, 
    feature_node,
    group_router, 
    group_node, 
    group_aggregate_node,
    permission_router, 
    permission_node, 
    permission_aggregate_node, 
    transform_permission_node,
    validation_node
)

logger = logging.getLogger(__name__)

def route_group_node(state: PipelineState, config: RunnableConfig) -> list[Send] | str:
    group_send_idx = state.get("group_send_idx", 0)
    llm_group_list: list[LLMWorker] = config["configurable"].get("llm_group_list", [])

    if group_send_idx < len(llm_group_list):
        llm = llm_group_list[group_send_idx]
        features = state["feature_result"].features

        sends = []
        for feat in features:
            sends.append(
                Send(
                    "group", 
                    {
                        "feature": feat,
                        "llm": llm
                    }
                )
            )

        logger.info(f"[Analyzing group assignments for {len(sends)} features using the {llm.config.model} model]")
        return sends
    else:
        return "group_arg"
    
def route_permission_node(state: PipelineState, config: RunnableConfig) -> list[Send] | str:
    permission_send_idx = state.get("permission_send_idx", 0)
    llm_permission_list: list[LLMWorker] = config["configurable"].get("llm_permission_list", [])

    if permission_send_idx < len(llm_permission_list):
        llm = llm_permission_list[permission_send_idx]
        features = state["feature_groups_aggregate_result"].features
    
        sends = []
        for feat in features:
            for inf in feat.inferences:
                if inf.group_name != "NONE":
                    sends.append(
                        Send(
                            "permission", 
                            {
                                "feature": feat,
                                "group_name": inf.group_name,
                                "llm": llm
                            }
                        )
                    )

        logger.info(f"[Analyzing permissions in {len(sends)} permission groups using the {llm.config.model} model]")
        return sends
    else:
        return "permission_arg"

def build_app():
    # Initialize the StateGraph with the PipelineState schema
    workflow = StateGraph(PipelineState)

    # Nodes
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("feature", feature_node)
    workflow.add_node("group_router", group_router)
    workflow.add_node("group", group_node)
    workflow.add_node("group_arg", group_aggregate_node)
    workflow.add_node("permission_router", permission_router)
    workflow.add_node("permission", permission_node)
    workflow.add_node("permission_arg", permission_aggregate_node)
    workflow.add_node("transform_permission", transform_permission_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("data_types", data_types_node)

    # Edges
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "feature")
    workflow.add_edge("feature", "group_router")
    workflow.add_edge("group", "group_router")
    workflow.add_edge("group_arg", "permission_router")
    workflow.add_edge("permission", "permission_router")
    workflow.add_edge("permission_arg", "transform_permission")
    workflow.add_edge("transform_permission", "validation")
    workflow.add_edge("validation", "data_types")
    workflow.add_edge("data_types", END)
    
    # Conditional edges
    workflow.add_conditional_edges(
        "group_router",
        route_group_node,
        {
            "group": "group",
            "group_arg": "group_arg"
        }
    )

    workflow.add_conditional_edges(
        "permission_router",
        route_permission_node,
        {   
            "permission": "permission",
            "permission_arg": "permission_arg"
        }
    )

    app = workflow.compile()

    # Create and save a graph 
    with open("pipeline_graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())

    return app 