import os
from openai import OpenAI

SYSTEM_PROMPT = """
Tu es N'FAYE, un assistant vocal francophone, utile, poli et pédagogique.
Réponds toujours en français simple, avec des explications claires et adaptées.
Sois concis lorsque la question est simple. N'invente pas de faits.
Si tu ne connais pas une réponse, dis-le clairement.
"""

def get_response(message: str) -> str:
    cleaned_message = (message or "").strip()

    if not cleaned_message:
        return "Écris ou dis-moi quelque chose pour commencer."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "La connexion à OpenAI n'est pas configurée. Ajoute OPENAI_API_KEY dans les variables d'environnement de Render."

    try:
        client = OpenAI(api_key=api_key)
        result = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
            instructions=SYSTEM_PROMPT,
            input=cleaned_message,
            max_output_tokens=800,
        )
        answer = (result.output_text or "").strip()
        return answer or "Je n'ai pas réussi à formuler une réponse. Peux-tu reformuler ?"
    except Exception as error:
        # Les détails techniques restent dans les journaux Render.
        print(f"Erreur OpenAI : {type(error).__name__}: {error}")
        return "Je rencontre un problème de connexion avec OpenAI. Vérifie la configuration puis réessaie."
