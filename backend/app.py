from fastapi import FastAPI
from backend.models.request_models import GenerateRequest
from backend.models.response_models import GenerateResponse
from backend.services.generator import generate_suggestion
from fastapi import HTTPException

app = FastAPI()

@app.get("/")
def home():
    return{"message":"backend is running successfully!!"}

@app.post("/generate", response_model=GenerateResponse)
def generate(request : GenerateRequest):
    try:
        suggestions = generate_suggestion(
            request.action,
            request.text
        )
        return{
            "action" : request.action,
            "text" : request.text,
            "suggestion" : suggestions
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
            )
