# IA Chatbot Python

Ce projet crée une IA de chat en Python capable de :
- démarrer une conversation interactive depuis le terminal
- créer automatiquement un fichier de conversation (`chat_history.json`)
- utiliser un modèle OpenAI si une clé API est fournie
- utiliser un mode local si aucune clé API n'est disponible
- se connecter à un serveur distant via HTTP (`!server http://localhost:8000/chat`)

## Structure

- `main.py` : interface interactive
- `assistant.py` : logique de l'IA, historique, connexion serveur
- `config.py` : paramètres de configuration
- `server_example.py` : exemple d'API serveur pour la connexion distante
- `requirements.txt` : dépendances Python

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
# ou .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Lancer le chatbot

```bash
python main.py
```

## Connecter un serveur distant

Dans le chatbot, tape :

```text
!server http://localhost:8000/chat
```

Le bot enverra alors une requête JSON au serveur.

## Exemple de serveur distant

```bash
pip install fastapi uvicorn
python server_example.py
```

Ou directement :

```bash
uvicorn server_example:app --reload
```

## Variables d'environnement (optionnel)

Crée un fichier `.env` :

```env
OPENAI_API_KEY=votre_cle
OPENAI_MODEL=gpt-4o-mini
SERVER_URL=http://localhost:8000/chat
HISTORY_FILE=chat_history.json
```

Si `OPENAI_API_KEY` n'est pas défini, le chatbot fonctionne en mode local.

## Exemple d'utilisation

```text
Vous > bonjour
IA > Bonjour ! Je suis ton assistant IA. Que puis-je faire pour toi ?

Vous > !server http://localhost:8000/chat

Vous > quel est le statut du serveur ?
IA > ...
```
