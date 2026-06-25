from pydantic import BaseModel, ConfigDict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable

class ConfiguredLLM(BaseModel):
    # Arbitrary types allowed for BaseChatModel and Runnable
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    model: str          
    temperature: float
    role: str
    instance: BaseChatModel | Runnable