import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from assistant import get_response

app = FastAPI(title="N'FAYE API", version="1.0.0")

# Pour un site hébergé ailleurs, définis FRONTEND_ORIGIN dans Render.
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*").strip() or "*"
allowed_origins = ["*"] if frontend_origin == "*" else [frontend_origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "N'FAYE backend fonctionne !",
        "provider": "Groq",
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        "api_key_configured": bool(os.getenv("GROQ_API_KEY", "").strip()),
    }


@app.post("/chat")
def chat(data: ChatMessage):
    return {"response": get_response(data.message)}
