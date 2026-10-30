# Backend N'FAYE

Backend Python basé sur FastAPI et connecté aux modèles GPT d'OpenAI via la Responses API.

## Variables d'environnement

Configure ces variables dans Render > service nfaye-api > Environment :

- `OPENAI_API_KEY` : clé API privée du projet OpenAI.
- `OPENAI_MODEL` : `gpt-5.5` par défaut.

Ne place jamais la vraie clé API dans GitHub, dans le code HTML ou dans un fichier public.

L'utilisation de l'API OpenAI est facturée séparément de l'abonnement ChatGPT. Vérifie les tarifs et les paramètres de facturation avant de l'activer.

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
