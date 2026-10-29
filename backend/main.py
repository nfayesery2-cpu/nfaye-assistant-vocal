from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from assistant import get_response

app = FastAPI(title="N'FAYE API", version="0.1.0")

# En production, remplace "*" par l'adresse exacte de ton site.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatMessage(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "N'FAYE backend fonctionne !"}

@app.post("/chat")
def chat(data: ChatMessage):
    return {"response": get_response(data.message)}
