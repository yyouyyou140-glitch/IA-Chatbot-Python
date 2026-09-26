import tkinter as tk
from tkinter import scrolledtext
from assistant import AIChatbot


class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Chatbot")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        self.bot = AIChatbot(history_file="chat_history.json")

        self.title_label = tk.Label(root, text="Assistant IA", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 5))

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 11))
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.entry = tk.Entry(self.input_frame, font=("Arial", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Envoyer", command=self.send_message, font=("Arial", 11), width=12)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.server_label = tk.Label(root, text="Serveur distant optionnel : ex. http://localhost:8000/chat", font=("Arial", 9))
        self.server_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.server_entry = tk.Entry(root, font=("Arial", 10))
        self.server_entry.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.connect_button = tk.Button(root, text="Connecter le serveur", command=self.connect_server, font=("Arial", 10))
        self.connect_button.pack(anchor="w", padx=15, pady=(0, 15))

        self.append_message("IA", "Bonjour ! Je suis ton assistant IA. Tu peux me parler ici.")

    def append_message(self, sender, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{sender} > {message}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def connect_server(self):
        server_url = self.server_entry.get().strip()
        if not server_url:
            self.append_message("IA", "Aucune URL de serveur fournie.")
            return

        self.bot.set_server(server_url)
        self.append_message("IA", f"Serveur connecté : {server_url}")

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if not message:
            return

        self.entry.delete(0, tk.END)
        self.append_message("Vous", message)

        if message.lower().startswith("!server "):
            url = message[8:].strip()
            if url:
                self.bot.set_server(url)
                self.append_message("IA", f"Serveur défini : {url}")
            else:
                self.append_message("IA", "Format invalide. Utilise : !server http://localhost:8000/chat")
            return

        if message.lower() == "!clear":
            self.bot.clear_history()
            self.append_message("IA", "Historique supprimé.")
            return

        if message.lower() == "!history":
            history = self.bot.show_history()
            if not history:
                self.append_message("IA", "Aucun historique pour le moment.")
            else:
                for item in history:
                    self.append_message(item["sender"], item["message"])
            return

        response = self.bot.ask(message)
        self.append_message("IA", response)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()
