from pydantic import BaseModel

class LLMConfig(BaseModel):
    
    model: str          
    temperature: float
    role: str