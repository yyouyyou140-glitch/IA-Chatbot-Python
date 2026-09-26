import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import requests

try:
    from openai import OpenAI
except ImportError:  # Optionnel : si tu n'as pas install openai
    OpenAI = None


HISTORY_FILE = "chat_history.json"


class ConversationManager:
    def __init__(self, history_file: str = HISTORY_FILE):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_file.exists():
            self.history_file.write_text("[]", encoding="utf-8")

    def load(self) -> List[Dict[str, str]]:
        try:
            with self.history_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            self.history_file.write_text("[]", encoding="utf-8")
            return []

    def save(self, messages: List[Dict[str, str]]) -> None:
        with self.history_file.open("w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

    def append(self, sender: str, message: str) -> None:
        messages = self.load()
        messages.append({"sender": sender, "message": message})
        self.save(messages)

    def clear(self) -> None:
        self.save([])

    def show(self) -> List[Dict[str, str]]:
        return self.load()


class AIChatbot:
    def __init__(
        self,
        history_file: str = HISTORY_FILE,
        server_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ):
        self.manager = ConversationManager(history_file)
        self.server_url = server_url or os.getenv("SERVER_URL")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and OpenAI else None

    def set_server(self, url: str) -> None:
        self.server_url = url

    def ask_server(self, message: str) -> Optional[str]:
        if not self.server_url:
            return None
        try:
            response = requests.post(
                self.server_url,
                json={"message": message},
                timeout=10,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict):
                for key in ("reply", "response", "message", "answer"):
                    if key in payload:
                        return str(payload[key])
                return json.dumps(payload, ensure_ascii=False)
            return str(payload)
        except Exception as exc:
            return f"Erreur de connexion au serveur: {exc}"

    def ask_openai(self, message: str) -> Optional[str]:
        if not self.client:
            return None
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es une IA utile, claire et concise."},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
            )
            return completion.choices[0].message.content
        except Exception as exc:
            return f"Erreur API OpenAI: {exc}"

    def generate_local_response(self, message: str) -> str:
        text = message.lower().strip()

        if "bonjour" in text or "salut" in text:
            return "Bonjour ! Je suis ton assistant IA. Que veux-tu faire ?"
        if "comment ca va" in text or "ça va" in text:
            return "Je vais très bien, merci ! Et toi ?"
        if "serveur" in text:
            return "Je peux aussi me connecter à un serveur distant via HTTP. Utilise !server http://localhost:8000/chat"
        if "heure" in text:
            import datetime
            return f"Il est {datetime.datetime.now().strftime('%H:%M:%S')}"
        if "date" in text:
            import datetime
            return f"Nous sommes le {datetime.datetime.now().strftime('%d/%m/%Y')}"
        if "help" in text or "aide" in text:
            return "Commandes: !server <url>, !history, !clear, !quit"

        return (
            "Je suis en mode local. "
            "Tu peux poser des questions, demander de l’aide, ou connecter un serveur distant."
        )

    def ask(self, message: str) -> str:
        self.manager.append("user", message)

        server_reply = self.ask_server(message)
        if server_reply:
            self.manager.append("assistant", server_reply)
            return server_reply

        openai_reply = self.ask_openai(message)
        if openai_reply:
            self.manager.append("assistant", openai_reply)
            return openai_reply

        local_reply = self.generate_local_response(message)
        self.manager.append("assistant", local_reply)
        return local_reply

    def clear_history(self) -> None:
        self.manager.clear()

    def show_history(self) -> List[Dict[str, str]]:
        return self.manager.show()


def main() -> None:
    print("===========================================")
    print("Assistant IA simple")
    print("===========================================")
    print("Commandes: !server <url>, !history, !clear, !quit")
    print("Le fichier de conversation est créé automatiquement: chat_history.json")

    bot = AIChatbot(history_file=HISTORY_FILE)

    while True:
        user_input = input("Vous > ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"!quit", "!exit", "quit", "exit", "bye"}:
            print("Au revoir !")
            break

        if user_input.lower() == "!history":
            history = bot.show_history()
            if not history:
                print("Aucun historique.")
            else:
                for item in history:
                    print(f"{item['sender']} > {item['message']}")
            continue

        if user_input.lower() == "!clear":
            bot.clear_history()
            print("Historique supprimé.")
            continue

        if user_input.lower().startswith("!server "):
            url = user_input[8:].strip()
            if not url:
                print("Utilisation: !server http://localhost:8000/chat")
                continue
            bot.set_server(url)
            print(f"Serveur connecté: {url}")
            continue

        response = bot.ask(user_input)
        print(f"IA > {response}")


if __name__ == "__main__":
    main()
