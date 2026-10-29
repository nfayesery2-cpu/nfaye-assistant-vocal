import os
from openai import OpenAI

SYSTEM_PROMPT = """
Tu es N'FAYE, un assistant vocal francophone, utile, poli et pédagogique.
Réponds en français simple, avec des explications claires et adaptées.
Sois concis lorsque la question est simple. N'invente pas de faits.
"""

def get_response(message: str) -> str:
    cleaned_message = message.strip()

    if not cleaned_message:
        return "Écris ou dis-moi quelque chose pour commencer."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "La connexion à l'intelligence artificielle n'est pas encore configurée. Ajoute la variable OPENAI_API_KEY dans les paramètres de Render."

    try:
        client = OpenAI(api_key=api_key)
        result = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=SYSTEM_PROMPT,
            input=cleaned_message,
        )
        answer = result.output_text.strip()
        return answer or "Je n'ai pas réussi à formuler une réponse. Peux-tu reformuler ?"
    except Exception:
        # Ne pas exposer les détails techniques ou secrets au navigateur.
        return "Je rencontre un problème de connexion pour le moment. Réessaie dans quelques instants."
