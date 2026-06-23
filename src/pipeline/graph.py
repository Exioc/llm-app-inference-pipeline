from langgraph.graph import StateGraph, START, END

from src.pipeline.state import PipelineState
from src.pipeline.nodes import preprocess_node, functionality_node, group_node, aggregate_node

from langgraph.constants import Send
from langchain_core.runnables import RunnableConfig
from src.pipeline.state import PipelineState
from src.schemas.llm_schema import ConfiguredLLM

# def route_groups_loop(state: PipelineState):
#     idx = state.get("current_group_index", 0)
#     total_features = len(state["functionality_result"].features)

#     if idx < total_features:
#         return "next_feature"
#     else:
#         return "finish"

def route_dynamic_group_nodes(state: PipelineState, config: RunnableConfig):
    llm_group_list: list[ConfiguredLLM] = config["configurable"].get("llm_group_list", [])
    send_commands = []
    
    for configured_llm in llm_group_list:
        # Wir isolieren den State für jedes LLM komplett
        node_state_arguments = {
            **state,
            "current_llm_model": configured_llm.model,
            "current_group_index": 0
            #"group_permissions_result": []
        }
        
        send_commands.append(Send("group", node_state_arguments))
        
    return send_commands

def decide_group_loop(state: PipelineState, config: RunnableConfig) -> str:
    current_idx = config["configurable"].get("current_branch_index", 0)
    #if current_idx < state.get("number_of_features", 0):
    if state.get("current_group_index", 0) < state.get("number_of_features", 0):
        return "loop"
    else:
        return "end"

def build_app():
    # Initialize the StateGraph with the PipelineState schema
    workflow = StateGraph(PipelineState)

    # Nodes
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)
    workflow.add_node("group", group_node)
    workflow.add_node("aggregate", aggregate_node)

    # Edges
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    #workflow.add_edge("function","group")
    workflow.add_edge("aggregate", END)
    
    # # Conditional Edges
    # workflow.add_conditional_edges(
    #     "group",      
    #     route_groups_loop,
    #     {
    #         "next_feature": "group", 
    #         "finish": END
    #     }
    # )

    workflow.add_conditional_edges(
        "function",
        route_dynamic_group_nodes,
        ["group"]
    )

    workflow.add_conditional_edges(
        "group",
        decide_group_loop,
        {
            "loop": "group",
            "end": "aggregate"    
        }
    )

    return workflow.compile()