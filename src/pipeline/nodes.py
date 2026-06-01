import base64
#from datetime import datetime

from src.pipeline.state import PipelineState
from src.utils.save_stage import save_stage
from src.prompts.functionality_prompts import FUNCTIONALITY_EXTRACTION_PROMPT
from src.models.llm import function_llm

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

    #now = datetime.now()
    #print(now.strftime("%H:%M:%S"))

    try:
        result = function_llm.invoke(messages)
    except Exception as e:
        print("LLM invocation or parsing failed:", repr(e))
        # Try to show raw LLM output if the parser attached it
        try:
            from langchain_core.exceptions import OutputParserException
            if isinstance(e, OutputParserException) and hasattr(e, 'llm_output'):
                print("Raw LLM output:\n", e.llm_output)
        except Exception:
            pass
        raise

    #now = datetime.now()
    #print(now.strftime("%H:%M:%S"))
    
    temp_state = {**state, **result.model_dump()}
    save_stage(temp_state, "02_functionality_extraction")

    return {"functionality_result": result}