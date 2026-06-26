from pydantic import BaseModel

class GenerateResponse(BaseModel):
    action : str
    text : str
    suggestion : list[str]