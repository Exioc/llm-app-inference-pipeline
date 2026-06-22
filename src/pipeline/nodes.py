import base64

from src.pipeline.state import PipelineState
from src.schemas.group_result_schema import PermissionGroupsContainer, PermissionGroupsResult
from src.utils.save_stage import save_stage
from src.prompts.func_prompt import FUNCTIONALITY_PROMPT
from src.prompts.group_prompt import GROUP_PROMPT
from src.models.llm import function_llm, group_llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from langgraph.constants import Send
import operator
from typing import Annotated, TypedDict
from src.schemas.llm_schema import ConfiguredLLM

def preprocess_node(state: PipelineState):
    metadata = state["metadata"]

    # Base64 Decoding
    def safe_decode(b64_str):
        try:
            return base64.b64decode(b64_str).decode('utf-8')
        except:
            return b64_str

    label = safe_decode(metadata.label)
    description = safe_decode(metadata.description.long)

    # Flatten permissions: Category -> List of strings
    flattened_perms = {
        item.category: item.permissions 
        for item in metadata.permissions
    }

    updates = {
        "pkg": metadata.pkg,
        "label": label,
        "description_long": description,
        "llmodel": state["llm_model"],
        "temperature": state["temperature"],
        "storage_path": state["storage_path"],
        "permissions_map": flattened_perms,
        "metadata": None
    }
    temp_state = {**state, **updates}
    save_stage(temp_state, "01_preprocessing")

    return updates
        

def functionality_node(state: PipelineState):
    messages = FUNCTIONALITY_PROMPT.invoke({
        "label": state["label"],
        "description": state["description_long"]
    })

    try:
        result = function_llm.invoke(messages)
    except Exception as e:
        print("LLM invocation or parsing failed:", repr(e))
        try:
            from langchain_core.exceptions import OutputParserException
            if isinstance(e, OutputParserException) and hasattr(e, 'llm_output'):
                print("Raw LLM output:\n", e.llm_output)
        except Exception:
            pass
        raise
    
    number = len(result.features)

    temp_state = {
        **state, 
        **result.model_dump(),
        "number_of_features": number
    }

    save_stage(temp_state, "02_functionality_extraction")

    return {
        "functionality_result": result,
        "number_of_features": number
    }

# def group_node(state: PipelineState, config: RunnableConfig) -> dict:
#     permission_groups = config["configurable"].get("permission_groups")
#     context_string = permission_groups.model_dump_json(indent=2)
    
#     idx = state["current_group_index"]
    
#     # Get the current feature
#     functionality_features = state["functionality_result"].features
#     current_feature = functionality_features[idx]

#     # Get previous group results to maintain state across iterations
#     current_group_results = state.get("group_permissions_result", {}).get("features", [])
#     updated_features = [item.copy() for item in current_group_results]

#     # LLM-call with context of all permission groups and the current feature
#     messages = GROUP_PROMPT.invoke({
#         "allowed_context": context_string,
#         "label": current_feature.functionality,
#         "description": current_feature.description
#     })
#     result = group_llm.invoke(messages)      
   
#     # Create a new entry for the current feature with its inferred permissions groups
#     new_feature_entry = {
#         "title": current_feature.functionality,       
#         "description": current_feature.description,   
#         "inferences": [item.model_dump() for item in result.inferences]
#     }
    
#     # Add the new feature entry to the list of features
#     updated_features.append(new_feature_entry)
    
#     # Return state
#     state_update = {
#         "group_permissions_result": {"features": updated_features},
#         "current_group_index": idx + 1
#     }

#     # Save state answer after last iteration
#     if state_update["current_group_index"] == state["number_of_features"]:
#         temp_state = {**state, **state_update}
#         save_stage(temp_state, "03_group_permission")

#     return state_update

# Nested Loop / Parallel-Map-with-Internal-Loop
def group_node(state: PipelineState, config: RunnableConfig) -> dict:
    permission_groups = config["configurable"].get("permission_groups")
    context_string = permission_groups.model_dump_json(indent=2)
    
    # 1. Dynamisches LLM für diesen spezifischen Ast holen
    target_model_name = state["current_llm_model"]
    llm_group_list: list[ConfiguredLLM] = config["configurable"].get("llm_group_list", [])
    chosen_llm = next((item for item in llm_group_list if item.model == target_model_name), None)
    group_llm = chosen_llm.instance 
    
    idx = config["configurable"].get("current_branch_index", 0)

    # 2. Aktuelles Feature holen
    #idx = state["current_group_index"]
    functionality_features = state["functionality_result"].features
    current_feature = functionality_features[idx]

    # Get previous group results to maintain state across iterations
    #current_group_results = state.get("group_permissions_result", {}).get("features", [])
    current_group_results = getattr(state.get("group_permissions_result"), "features", [])
    updated_features = [item.copy() for item in current_group_results]

    # --- LLM Aufruf ---
    messages = GROUP_PROMPT.invoke({
        "allowed_context": context_string,
        "label": current_feature.functionality,
        "description": current_feature.description
    })
    result = group_llm.invoke(messages)      
   
    # 4. Neuen Eintrag für das aktuelle Feature erstellen
    new_feature_entry = {
        "title": current_feature.functionality,       
        "description": current_feature.description,
        "inferred_by_model": target_model_name,   
        "inferences": [item.model_dump() for item in result.inferences]
    }
    
    # Das neue Feature an die Historie DIESES Modells anhängen
    updated_features.append(new_feature_entry)
    
    state_update = {
        "group_permissions_result": PermissionGroupsResult(features=updated_features),
        "current_llm_model": target_model_name
        #"current_group_index": idx + 1
    }
    next_idx = idx + 1
    config["configurable"]["current_branch_index"] = next_idx

    # 6. Deine originale Speicher-Logik nach der letzten Iteration dieses Modells
    #if state_update["current_group_index"] == state["number_of_features"]:
    if next_idx == state["number_of_features"]:
        temp_state = {**state, **state_update}
        # Wir hängen den Modellnamen an den Dateinamen, damit sich die Speicherstände nicht überschreiben
        save_stage(temp_state, f"{target_model_name}", True)
        
    return state_update

def aggregate_node(state: PipelineState) -> dict:
    # Hier kommen ALLE Ergebnisse aller Modelle zusammen!
    all_inferences = state.get("group_permissions_result", [])
    
    print(f"Aggriere {len(all_inferences)} Ergebnisse aus den parallelen LLM-Läufen...")
    
    # Beispiel-Logik: Gruppiere die Vorhersagen nach Feature-Titel
    aggregated_features = {}
    for entry in all_inferences:
        title = entry["title"]
        if title not in aggregated_features:
            aggregated_features[title] = {
                "title": title,
                "description": entry["description"],
                "raw_model_outputs": []
            }
        
        # Sammle, welches Modell welche Inferences gezogen hat
        aggregated_features[title]["raw_model_outputs"].append({
            "model": entry["inferred_by_model"],
            "inferences": entry["inferences"]
        })
    
    # Hier kannst du jetzt ein finales "Mehrheits-Voting" berechnen 
    # oder die Daten für dein finales JSON-Schema aufbereiten.
    final_features_list = list(aggregated_features.values())
    
    # Wir speichern das bereinigte, finale Ergebnis in einem neuen State-Key ab
    return {
        "final_aggregated_result": final_features_list
    }