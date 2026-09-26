import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    def __init__(self):
        self.HISTORY_FILE = os.getenv("HISTORY_FILE", "chat_history.json")
        self.SERVER_URL = os.getenv("SERVER_URL", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ensure_paths(self):
        Path(self.HISTORY_FILE).parent.mkdir(parents=True, exist_ok=True)
        path = Path(self.HISTORY_FILE)
        if not path.exists():
            path.write_text("[]", encoding="utf-8")


settings = Settings()
settings.ensure_paths()
