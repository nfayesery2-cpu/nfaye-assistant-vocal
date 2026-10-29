# Backend N'FAYE

Backend Python basé sur FastAPI.

## Installation locale

Depuis le dossier du dépôt :

```bash
python -m venv .venv
```

Active l'environnement virtuel, puis installe les dépendances :

```bash
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

La connexion OpenAI sera ajoutée dans une prochaine étape. Ne publie jamais une vraie clé API dans Git.
