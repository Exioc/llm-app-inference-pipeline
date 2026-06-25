import logging
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

from src.schemas.llm import ConfiguredLLM
from src.pipeline.state import PipelineState
from src.pipeline.nodes import preprocess_node, functionality_node, group_node, aggregate_node

logger = logging.getLogger(__name__)

def route_to_all_models_and_features(state: PipelineState, config: RunnableConfig) -> list[Send]:

    # Get the list of configured LLMs from the config
    llm_group_list: list[ConfiguredLLM] = config["configurable"].get("llm_group_list", [])
    model_names = [llm.model for llm in llm_group_list]
    
    # Get the number of features to process from the state
    num_features = state.get("number_of_features", 0)
    
    sends = []
    
    # Cross product of model names and feature indices to create Send objects for each combination
    for model_name in model_names:
        for idx in range(num_features):
            sends.append(
                Send(
                    "group", 
                    {   **state,
                        "current_llm_model": model_name,
                        "current_feature_index": idx
                    }
                )
            )
            
    logger.info(f"Analyzing groups via {len(sends)} parallel instances across {len(model_names)} LLM models.")
    return sends


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
    workflow.add_edge("group", "aggregate")
    workflow.add_edge("aggregate", END)
    
    # Conditional edges
    workflow.add_conditional_edges(
        "function",
        route_to_all_models_and_features,
        {"group": "group"}
    )

    return workflow.compile()