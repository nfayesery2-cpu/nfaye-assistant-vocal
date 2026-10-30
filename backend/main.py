import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from assistant import get_response

app = FastAPI(title="N'FAYE API", version="1.1.0")
FRONTEND_FILE = Path(__file__).resolve().parent.parent / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "N'FAYE fonctionne !",
        "provider": "Groq",
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        "api_key_configured": bool(os.getenv("GROQ_API_KEY", "").strip()),
    }


@app.post("/chat")
def chat(data: ChatMessage):
    return {"response": get_response(data.message)}
