import os
import logging
from openai import OpenAI

logger = logging.getLogger("nfaye")

SYSTEM_PROMPT = """
Tu es N'FAYE, un assistant vocal francophone, utile, poli et pédagogique.
Réponds toujours en français simple, avec des explications claires et adaptées.
Sois concis lorsque la question est simple. N'invente pas de faits.
Si tu ne connais pas une réponse, dis-le clairement.
"""


def get_response(message: str) -> str:
    cleaned_message = (message or "").strip()

    if not cleaned_message:
        return "Dis-moi quelque chose pour commencer."

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        logger.error("GROQ_API_KEY est absente de l'environnement.")
        return "La connexion à Groq n'est pas configurée. Ajoute GROQ_API_KEY dans Render, section Environment."

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
    if not model:
        model = "openai/gpt-oss-120b"

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0,
            max_retries=1,
        )
        result = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=cleaned_message,
            max_output_tokens=800,
        )
        answer = (result.output_text or "").strip()
        if not answer:
            logger.warning("Groq a renvoyé une réponse vide (modèle : %s).", model)
            return "Je n'ai pas reçu de réponse. Peux-tu reformuler ta question ?"
        return answer

    except Exception:
        # Ne jamais écrire la clé API dans les journaux.
        logger.exception("Échec de l'appel à l'API Groq (modèle : %s).", model)
        return "Je rencontre un problème avec le service IA. Vérifie la clé Groq, le modèle configuré et les journaux Render."
