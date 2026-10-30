import os
from pathlib import Path
import io
from typing import Literal

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.assistant import get_response

app = FastAPI(title="N'FAYE API", version="1.2.0")
FRONTEND_FILE = Path(__file__).resolve().parent.parent / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    history: list[HistoryMessage] = Field(default_factory=list, max_length=12)
    input_mode: Literal["text", "voice"] = "text"


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
    history = [item.model_dump() for item in data.history]
    return {"response": get_response(data.message, history, data.input_mode)}


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """Transcrit un enregistrement vocal lorsque la reconnaissance du navigateur échoue."""
    content_type = (audio.content_type or "").lower()
    if not (content_type.startswith("audio/") or "webm" in content_type or "mp4" in content_type):
        raise HTTPException(status_code=415, detail="Format audio non pris en charge.")
    payload = await audio.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Aucun son reçu.")
    if len(payload) > 20 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Enregistrement trop volumineux (20 Mo maximum).")
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="La clé Groq n'est pas configurée.")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1", timeout=60.0, max_retries=1)
        filename = "audio.webm" if "webm" in content_type else "audio.mp4"
        result = client.audio.transcriptions.create(
            model=os.getenv("GROQ_STT_MODEL", "whisper-large-v3-turbo"),
            file=(filename, io.BytesIO(payload), audio.content_type or "audio/webm"),
            language="fr",
            response_format="json",
        )
        text = (getattr(result, "text", "") or "").strip()
        if not text:
            raise HTTPException(status_code=422, detail="Aucune parole claire détectée.")
        return {"text": text}
    except HTTPException:
        raise
    except Exception as exc:
        import logging
        logging.getLogger("nfaye").exception("Échec de transcription audio (%s).", type(exc).__name__)
        raise HTTPException(status_code=502, detail="La transcription vocale est momentanément indisponible.")
