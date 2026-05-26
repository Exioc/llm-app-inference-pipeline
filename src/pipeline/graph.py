from langgraph.graph import StateGraph, START, END

from src.pipeline.state import PipelineState
from src.pipeline.nodes import preprocess_node, functionality_node

def build_app():
    # 1. Initialisierung mit dem State-Schema
    workflow = StateGraph(PipelineState)

    # 2. Nodes registrieren
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)

    # 3. Kanten (Edges) ziehen
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("function", END)

    # 4. Kompilieren (Das macht den Graph ausführbar)
    app = workflow.compile()
    
    return workflow.compile()