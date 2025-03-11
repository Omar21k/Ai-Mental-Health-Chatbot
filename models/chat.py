from typing import Dict, List

class ChatManager:
    def __init__(self):
        self.DEFAULT_QUOTES = [
            "Every day is a new beginning. Take a deep breath and start again.",
            "You are stronger than you know.",
            "One step at a time, one day at a time.",
            "Your feelings matter, and you're not alone."
        ]

    def get_default_quote(self):
        import random
        return random.choice(self.DEFAULT_QUOTES)

    def generate_quote_prompt(self, message, mood):
        return f"Generate an inspirational quote relevant to someone feeling {mood}. Context: {message}"

chat_manager = ChatManager()
