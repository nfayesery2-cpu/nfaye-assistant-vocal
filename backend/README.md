# Backend N'FAYE

Backend Python avec FastAPI, connecté à **OpenAI GPT-OSS 120B hébergé par Groq**.

L'intégration utilise le client Python OpenAI avec l'URL compatible Groq :
`https://api.groq.com/openai/v1`, et l'API Responses.

## Configuration sur Render

Dans Render > service `nfaye-api` > Environment, configure :

- `GROQ_API_KEY` : clé API privée créée dans ton espace Groq.
- `GROQ_MODEL` : `openai/gpt-oss-120b`.
- `FRONTEND_ORIGIN` : facultatif, adresse exacte du site web si tu souhaites limiter les origines autorisées.

Ne publie jamais la vraie clé API dans GitHub, dans le code HTML ou dans un fichier public.

Après avoir modifié les variables, sauvegarde et attends la fin du déploiement.

## Installation locale

Depuis le dossier du dépôt :

```bash
python -m venv .venv
pip install -r requirements.txt
```

Démarre le serveur depuis le dossier `backend` :

```bash
uvicorn main:app --reload
```

L'API sera disponible sur http://127.0.0.1:8000 et sa documentation sur
http://127.0.0.1:8000/docs.

## Vérification

- `GET /` : vérifie le serveur et indique si `GROQ_API_KEY` est configurée.
- `POST /chat` : reçoit `{"message":"Bonjour N'FAYE" }` et renvoie `{"response":"..." }`.

Si l'API répond que la clé n'est pas configurée, vérifie les variables Render.
Si le serveur ne démarre pas, consulte les journaux de déploiement Render.
