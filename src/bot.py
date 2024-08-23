import os
from datetime import datetime

from models import get_models
from utils import load_files, save_messages


class ChatBot:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.models = get_models(include_chat=True)
        self.assistants = load_files(path=self.cfg["paths"]["assistants"], add_created_datetime=False)
        if "history" in self.cfg:
            self.new_chat_id = "New chat"
            self.history_id = self.new_chat_id
            self._history = load_files(path=self.cfg["paths"]["history"], add_created_datetime=True)
            self.add_new_chat()

    def add_new_chat(self):
        key_order = [self.new_chat_id] + [k for k in self._history]
        self._history[self.new_chat_id] = {
            "content": [{"role": "assistant", "content": "Hi, how I help you today?"}],
            "date": datetime.now(),
        }
        self._history = {k: self._history[k] for k in key_order}

    async def rename_history_id(self, msg: dict):
        if self.history_id == self.new_chat_id:
            model = self.models["chat"][self.cfg["models"]["chat"]]
            instruction = {
                "role": "system",
                "content": "Return a very short title for based on the following question",
            }
            messages = [msg, instruction]
            new_history_id = model(messages=messages).choices[0].message.content.strip()
            new_history_id = "".join(char for char in new_history_id if char.isalnum() or char == " ")
            self._history[new_history_id] = self._history.pop(self.history_id)
            key_order = [new_history_id] + [k for k in self._history if k != new_history_id]
            self._history = {k: self._history[k] for k in key_order}
            self.history_id = new_history_id
            self.add_new_chat()

    def chat(self, user_input: str, history_size: int = None) -> str:
        """Sends user_input to the bot, and then adds the response dict to chat_history and returns the answer as str"""
        question = {"role": "user", "content": user_input}
        messages = self.compile_messages(question, history_size=history_size)
        model = self.models["chat"][self.cfg["models"]["chat"]]
        response = {"role": "assistant", "content": model(messages=messages).choices[0].message.content}
        self.history += [question, response]
        if self.cfg["history"].get("auto_save") is True:
            self.save_messages()
        return response["content"]

    async def async_chat(self, *args, **kwargs) -> str:
        """Asynchronous version of chat()"""
        return self.chat(*args, **kwargs)

    @property
    def history(self) -> list:
        return self._history[self.history_id]["content"]

    @history.setter
    def history(self, value: list) -> None:
        self._history[self.history_id]["content"] = value

    @property
    def history_ids(self) -> list:
        return list(self._history)

    def save_messages(self) -> None:
        history_path = self.cfg["paths"]["history"]
        filename = f"{self.history_id}.yaml"
        save_messages(self.history, path=os.path.join(history_path, filename))

    def compile_messages(self, question: dict, history_size: int = None) -> list:
        """Compile instructions + history + question"""
        instruction = {"role": "system", "content": self.assistants[self.cfg["assistant"]]}
        history = self.history
        if "history" in self.cfg:
            history_size = self.cfg["history"]["size"] if history_size is None else history_size
            history = history if history_size is None else history[-history_size:]
        return [instruction] + history + [question]
