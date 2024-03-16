import os
import json

from models import get_model, models
from config import load_cfg

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"


class ChatBot:
    def __init__(self, cfg: dict = load_cfg()):
        self.cfg = cfg
        self.models = models
        self.bots = self.load_bots()
        self.chat_history = self.load_history()

    def get_response(self, user_input: str) -> str:
        question = {"role": "user", "content": user_input}
        msgs = self.get_msgs(question, history_size=self.cfg["history_size"])
        model = get_model(self.cfg["model"])
        answer = model(messages=msgs).choices[0].message
        self.chat_history.extend([question, answer])
        return answer.content

    def get_msgs(self, question: dict, history_size: int = 10) -> list:
        """Get messages for bot to respond to"""
        instruction = {"role": "system", "content": self.bots[self.cfg["bot"]]}
        history = self.chat_history[-history_size:] if history_size else self.chat_history
        return [instruction] + history + [question]

    def load_bots(self) -> dict:
        """Load bots from files"""
        path = self.cfg["dirs"]["bots"]
        bots = {}
        for filename in os.listdir(ROOT_PATH + path):
            with open(ROOT_PATH + path + filename, "r") as f:
                bots[filename.removesuffix(".txt")] = f.read()
        return bots

    def load_history(self) -> list:
        """Load chat history from file"""
        path = f"{self.cfg['dirs']['history']}{self.cfg['history']}.json"
        history = []
        if os.path.exists(ROOT_PATH + path) is True:
            with open(ROOT_PATH + path, "r") as f:
                history = json.load(f)
        return history
