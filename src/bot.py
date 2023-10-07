import cmd

from model import get_model
from messages import (
    load_prompt,
    load_history,
    get_question,
    get_answer,
    get_msgs,
    print_history,
    save_history,
    save_msg,
)
from config import cfg as default_cfg
from config import save_cfg, print_cfg


class ChatBot(cmd.Cmd):
    intro = "Entering chat session: type '/h' for help, '/c' for commands, '/q' to quit"
    prompt = "> "
    last_line = ""

    def __init__(self, cfg: dict = default_cfg):
        super().__init__()
        self.cfg = cfg
        self.model = get_model(model_name=self.cfg["model"], env_filename=self.cfg["files"]["env"])
        self.chat_prompt = load_prompt(path=self.cfg["dirs"]["prompt"], filename=f"{self.cfg['prompt']}.txt")
        self.chat_history = load_history(path=self.cfg["dirs"]["history"], filename=f"{self.cfg['history']}.json")

        # Add aliases for commands
        self.commands = {
            ChatBot.do_commands: ["c", "commands"],
            ChatBot.do_help: ["h", "help"],
            ChatBot.do_save: ["s", "save"],
            ChatBot.do_config: ["cfg", "config"],
            ChatBot.do_history: ["hs", "history"],
            ChatBot.do_quit: ["q", "quit", "exit"],
        }
        for func, commands in self.commands.items():
            for command in commands:
                setattr(ChatBot, f"do_{command}", func)

    def parseline(self, line: str):
        """Override parseline to allow for '/' commands"""
        if line.startswith("/"):
            return super().parseline(line[1:])
        return None, None, line

    def do_quit(self, _arg):
        """Quit chat session: /q, /quit, /exit"""
        if self.cfg["save_history_on_exit"] is True:
            save_history(self.chat_history, path=self.cfg["dirs"]["history"], filename=f"{self.cfg['history']}.json")
        if self.cfg["save_config_on_exit"] is True:
            save_cfg(self.cfg)
        return True

    def do_save(self, filename: str = None):
        """Save the last line written in console to file: /save <filename: str>"""
        save_msg(self.last_line, path=self.cfg["dirs"]["saved"], filename=filename)

    def do_history(self, i: int = None):
        """Print chat history: /history <i: int>"""
        chat_history = self.chat_history or [{"content": "No chat history"}]
        try:
            chat_history = [chat_history[-1 * int(i)]] if i else chat_history
        except IndexError:
            return print(f"IndexError: index {i} out of range for {len(chat_history)=}")
        self.last_line = chat_history[-1]["content"]
        print_history(chat_history)

    def do_config(self, arg: str = None) -> None:
        """Set config values: /config <key: str>=<value: str>"""
        if not arg:
            return print_cfg(self.cfg)

        args = arg.split("=")
        key, value = args[0], args[1]

        # Key validation
        if key not in self.cfg:
            print(f"{key=} not found in cfg:\n")
            print_cfg(self.cfg)
            return
        try:
            if key == "prompt":
                self.chat_prompt = load_prompt(path=self.cfg["dirs"]["prompt"], filename=f"{value}.txt")
            elif key == "history":
                self.chat_history = load_history(path=self.cfg["dirs"]["history"], filename=f"{value}.json")
            elif key == "model":
                self.model = get_model(model_name=value, env_filename=self.cfg["files"]["env"])
        except FileNotFoundError:
            return print(f"file '{self.cfg['paths'][key]}{value}.*' not found")

        # Value validation
        if value.lower() in ["true", "false"]:
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)

        # Set new config value
        self.cfg[key] = value

        print_cfg(self.cfg)

    def do_commands(self, _arg):
        """View available commands: /commands, /c"""
        for func, aliases in self.commands.items():
            print(f"{func.__name__.split('_')[1]}: {[f'/{a}' for a in aliases]}")

    def default(self, line):
        """Default cmdloop: Get question from user and answer from bot"""
        question = get_question(line)
        msgs = get_msgs(self.chat_prompt, self.chat_history, question, history_size=self.cfg["history_size"])
        answer = get_answer(msgs, model=self.model)
        self.chat_history.extend([question, answer])
        self.last_line = answer["content"]
