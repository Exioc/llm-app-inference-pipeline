from langgraph.graph import StateGraph, START, END

from src.pipeline.state import PipelineState
from src.pipeline.nodes import preprocess_node, functionality_node, state_transformer_node, group_filter_node, save_groups_node

def route_groups_loop(state: PipelineState):
    idx = state.get("current_group_index", 0)
    total_features = len(state["group_permissions_result"]["features"])

    if idx < total_features:
        return "next_feature"
    else:
        return "finish"

def build_app():
    # Initialize the StateGraph with the PipelineState schema
    workflow = StateGraph(PipelineState)

    # Nodes
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)
    workflow.add_node("transformer", state_transformer_node)
    workflow.add_node("group", group_filter_node)
    workflow.add_node("save_groups", save_groups_node)

    # Edges
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("function", "transformer")
    workflow.add_edge("transformer", "group")
    workflow.add_edge("save_groups", END)

    # Conditional Edges
    workflow.add_conditional_edges(
        "group",      
        route_groups_loop,
        {
            "next_feature": "group", 
            "finish": "save_groups"
        }
    )

    return workflow.compile()