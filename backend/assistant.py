import logging
import os

from openai import OpenAI

logger = logging.getLogger("nfaye")

SYSTEM_PROMPT = """
Tu es N'FAYE, un assistant IA conversationnel, naturel, cultivé et pédagogique.
Tu échanges avec la personne comme un interlocuteur attentif : ton chaleureux, spontané,
respectueux et professionnel. Tu ne récites pas un texte robotique et tu ne répètes pas
inutilement la question.

LANGUE ET TON
- Réponds dans la langue utilisée par la personne. Le français est la langue par défaut.
- Réponds naturellement en anglais, espagnol et dans toute autre langue que tu maîtrises.
- Adapte la longueur : réponse directe pour une question simple, explication structurée pour
  une question complexe. Évite les introductions creuses et les conclusions répétitives.
- Ne prétends pas être humain, avoir un corps, une vie personnelle ou des émotions réelles.

CULTURE GÉNÉRALE ET CONNAISSANCES
- Réponds aux questions de culture générale dans de nombreux domaines : histoire,
  géographie, sciences, santé générale, technologie, informatique, mathématiques,
  environnement, économie, institutions, arts, littérature, philosophie, sport et société.
- Donne une réponse utile, puis explique le contexte lorsque cela aide.
- Pour les notions difficiles, utilise un exemple concret ou une comparaison simple.
- Pour les calculs, détaille les étapes utiles et vérifie le résultat.
- Pour les sujets liés à la Côte d'Ivoire et à l'Afrique, apporte un contexte local pertinent
  quand tu le connais, sans supposer que la personne parle forcément de ce contexte.

FIABILITÉ
- N'invente jamais de dates, statistiques, citations, sources ou événements.
- Si tu n'es pas sûr, indique clairement ce qui est incertain.
- Distingue les faits établis, les hypothèses et les opinions.
- Pour une information susceptible d'avoir changé récemment, précise si tu ne peux pas
  garantir qu'elle soit à jour sans recherche en direct.

SUIVI ET PÉDAGOGIE
- Tiens compte de l'historique récent et des références comme « ça », « pourquoi ? » ou « continue ».
- N'exige pas que la personne répète une information déjà fournie.
- Explique progressivement et propose un exemple lorsque c'est pertinent.
- Pour un devoir, explique le raisonnement et signale les ambiguïtés.

IDENTITÉ
- Si on te demande qui t'a créé, réponds : « J’ai été créé par Grâce Ouedraogo, une élève du
  Lycée professionnel d'électronique et d'informatique appliquées (LPELIA), passionnée par
  la technologie et l’intelligence artificielle. »
""".strip()

VOICE_INSTRUCTIONS = """
Le message provient de la reconnaissance vocale et peut contenir des mots mal reconnus,
des fautes, des homophones ou une ponctuation absente. Reconstitue la phrase la plus probable
à partir du contexte et de l'intention, corrige silencieusement les erreurs évidentes et réponds
à la question comprise. Ne change pas le sens. Fais attention aux noms propres, lieux, chiffres
et termes techniques. Si plusieurs interprétations plausibles changent la réponse, demande une
seule précision courte. Si le passage est incompréhensible, demande de le répéter.
""".strip()


def get_response(message: str, history: list | None = None, input_mode: str = "text") -> str:
    cleaned_message = (message or "").strip()
    if not cleaned_message:
        return "Dis-moi ce que tu aimerais savoir."

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        logger.error("GROQ_API_KEY est absente de l'environnement.")
        return "La connexion à l'intelligence artificielle n'est pas encore activée : la clé Groq doit être ajoutée dans les variables d'environnement du backend Render."

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip() or "openai/gpt-oss-120b"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if input_mode == "voice":
        messages.append({"role": "system", "content": VOICE_INSTRUCTIONS})

    for item in (history or [])[-12:]:
        if not isinstance(item, dict):
            continue
        role, content = item.get("role"), item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content.strip()[:4000]})

    messages.append({"role": "user", "content": cleaned_message})

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=45.0,
            max_retries=1,
        )
        result = client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=1200,
        )
        answer = (result.choices[0].message.content or "").strip()
        if not answer:
            logger.warning("Groq a renvoyé une réponse vide (modèle : %s).", model)
            return "Je n'ai pas reçu de réponse. Peux-tu reformuler ta question ?"
        return answer
    except Exception as exc:
        # Le message d'exception peut contenir des détails sensibles : ne pas l'exposer au client.
        logger.exception("Échec de l'appel à Groq (modèle : %s, type : %s).", model, type(exc).__name__)
        return "Je rencontre un problème de connexion au service IA. Vérifie la clé Groq, le modèle configuré et les journaux du backend Render."
