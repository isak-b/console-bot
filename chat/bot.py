from models import get_models
from utils import load_cfg, load_bots


class ChatBot:
    def __init__(self, cfg: dict = None):
        self.cfg = cfg or load_cfg()
        self.bots = load_bots(bots_path=self.cfg["paths"]["bots"])
        self.chat_models = get_models(include_chat=True)["chat"]
        self.chat_history = []

    def chat(self, user_input: str, history_size: int = None) -> str:
        """Sends user_input to the bot, and then adds the response dict to chat_history and returns the answer as str"""
        question = {"role": "user", "content": user_input}
        messages = self.compile_messages(question, history_size=history_size)
        model = self.chat_models[self.cfg["model"]]
        response = {"role": "assistant", "content": model(messages=messages).choices[0].message.content}
        self.chat_history.extend([question, response])
        return response["content"]

    async def async_chat(self, *args, **kwargs) -> str:
        """Asynchronous version of chat()"""
        return self.chat(*args, **kwargs)

    def compile_messages(self, question: dict, history_size: int = None) -> list:
        """Compile instructions + history + question"""
        instruction = {"role": "system", "content": self.bots[self.cfg["bot"]]}
        history_size = self.cfg["history_size"] if history_size is None else history_size
        history = self.chat_history[-history_size:] if history_size else self.chat_history
        return [instruction] + history + [question]
