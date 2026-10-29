def get_response(message: str) -> str:
    """Réponse temporaire en attendant la connexion à l'API OpenAI."""
    cleaned_message = message.strip()

    if not cleaned_message:
        return "Écris ou dis-moi quelque chose pour commencer."

    lowered = cleaned_message.lower()

    if any(word in lowered for word in ["bonjour", "salut", "bonsoir"]):
        return "Bonjour ! Je suis N'FAYE, ton assistant vocal. Comment puis-je t'aider ?"

    return (
        "J'ai bien reçu ton message : "
        f"{cleaned_message}. "
        "Ma connexion à ChatGPT sera activée dans une prochaine étape."
    )
