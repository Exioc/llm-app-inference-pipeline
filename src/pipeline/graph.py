from langgraph.graph import StateGraph, START, END

from src.pipeline.state import PipelineState
from src.pipeline.nodes import preprocess_node, functionality_node, group_node

def route_groups_loop(state: PipelineState):
    idx = state.get("current_group_index", 0)
    total_features = len(state["functionality_result"].features)

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
    workflow.add_node("group", group_node)

    # Edges
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("function","group")
    
    # Conditional Edges
    workflow.add_conditional_edges(
        "group",      
        route_groups_loop,
        {
            "next_feature": "group", 
            "finish": END
        }
    )

    return workflow.compile()