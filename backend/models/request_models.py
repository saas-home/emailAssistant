from pydantic import BaseModel

class GenerateRequest(BaseModel):
    action : str
    text : str