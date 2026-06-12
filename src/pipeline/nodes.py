import base64

#from src.pipeline.state import PipelineState, PermissionGroupsContainer, PermissionGroupsResult
from src.pipeline.state import PipelineState
from src.schemas.permissions_groups import PermissionGroupsContainer, PermissionGroupsResult
from src.utils.save_stage import save_stage
from src.prompts.functionality_prompt import FUNCTIONALITY_EXTRACTION_PROMPT
from src.prompts.permission_groups_prompt import PERMISSION_GROUPS_PROMPT
from src.models.llm import function_llm, group_llm
from langchain_core.prompts import ChatPromptTemplate

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
    messages = FUNCTIONALITY_EXTRACTION_PROMPT.invoke({
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
    
    temp_state = {**state, **result.model_dump()}
    save_stage(temp_state, "02_functionality_extraction")

    return {"functionality_result": result}

def state_transformer_node(state: PipelineState):
    transformed_features = []
    
    func_result = state["functionality_result"]
    
    for full_feature in func_result.features:
        clean_container = PermissionGroupsContainer(
            title=full_feature.functionality, 
            description=full_feature.description,
            groups=[]
        )
        transformed_features.append(clean_container)
        
    wrapped_result = PermissionGroupsResult(features=transformed_features)
    
    state_update = {
        "group_permissions_result": wrapped_result.model_dump(),
        "current_group_index": 0 
    }
    
    temp_state = {**state, **state_update}
    save_stage(temp_state, "03_state_transformation")
    
    return state_update

def group_filter_node(state: PipelineState) -> dict:

    # Get the current feature index and the corresponding feature details from the state
    idx = state["current_group_index"]
    features_list = state["group_permissions_result"]["features"]
    current_feature = features_list[idx]

    messages = PERMISSION_GROUPS_PROMPT.invoke({
        "label": current_feature["title"],
        "description": current_feature["description"]
    })

    result = group_llm.invoke(messages)      
   
    updated_features = [item.copy() for item in features_list]
    
    updated_features[idx]["groups"] = result.groups
    
    state_update = {
        "group_permissions_result": {"features": updated_features},
        "current_group_index": idx + 1
    }
    
    return state_update

def save_groups_node(state: PipelineState):
    save_stage(state, "04_group_permission")
    return {}