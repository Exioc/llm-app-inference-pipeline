from typing import TypedDict, Optional, List, Any
from pydantic import BaseModel, Field

class FeatureExtraction(BaseModel):
    """Einzelne Funktionalität mit Begründung."""
    functionality: str = Field(description="Name der extrahierten Funktionalität")
    description: str = Field(description="Kurze Beschreibung, was die Funktion tut")
    reasoning: str = Field(description="Textpassage und logische Herleitung, warum diese Funktion existiert")

class AppAnalysis(BaseModel):
    """Das finale JSON-Format."""
    features: List[FeatureExtraction] = Field(description="Liste aller extrahierten Funktionalitäten")

# PipelineState (TypedDict)
class PipelineState(TypedDict, total=False):
    # Path/Timestamp 
    run_dir: str

    #Template
    template_name: str

    #LLM
    llm_model: str

    # Input Felder
    app_title: str
    app_description: str
    
    # Ergebnisse der Stufen
    stage1_result: str
    stage2_result: AppAnalysis
    stage3_result: str
