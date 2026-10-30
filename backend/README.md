# Backend N'FAYE

Backend Python basé sur FastAPI et connecté à Groq.

## Variables d'environnement

Configure ces variables dans Render > service nfaye-api > Environment :

- `GROQ_API_KEY` : clé API privée créée dans GroqCloud.
- `GROQ_MODEL` : `llama-3.3-70b-versatile` (valeur par défaut).

Ne place jamais la vraie clé API dans GitHub, dans le code HTML ou dans un fichier public.

## Installation locale

Depuis le dossier du dépôt :

```bash
python -m venv .venv
pip install -r backend/requirements.txt
```

Démarre le serveur depuis le dossier `backend` :

```bash
uvicorn main:app --reload
```

L'API sera disponible sur http://127.0.0.1:8000 et sa documentation sur
http://127.0.0.1:8000/docs.

## Routes

- `GET /` : vérifie que le serveur fonctionne.
- `POST /chat` : reçoit un JSON contenant `message` et renvoie `response`.
