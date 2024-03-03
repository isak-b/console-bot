from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

from model import get_model, models
from messages import (
    load_instruction,
    load_history,
    get_question,
    get_answer,
    get_msgs,
    save_history,
    save_msg,
)
from config import cfg_path, load_cfg, save_cfg, parse_cfg_kwargs
from utils import get_formatted_dict

default_cfg = load_cfg()


class ChatBot:
    def __init__(self, cfg: dict = default_cfg):
        super().__init__()
        self.cfg = cfg
        self.model = get_model(model_name=self.cfg["model"], env_filename=self.cfg["files"]["env"])
        self.instruction = load_instruction(path=f"{self.cfg['dirs']['bots']}{self.cfg['bot']}.txt")
        self.chat_history = load_history(path=f"{self.cfg['dirs']['history']}{self.cfg['history']}.json")
        self.style = Style.from_dict({k: "" if v is None else v for k, v in self.cfg["style"].items()})
        self.user_commands = {
            self.do_config: ["config", "cfg"],
            self.do_view_commands: ["commands", "c"],
            self.do_save_message: ["save", "s"],
            self.do_view_history: ["history", "hs"],
            self.do_save_history: ["save_history", "save_hs"],
            self.do_clear_history: ["clear_history", "clear_hs"],
            self.do_quit: ["quit", "q", "exit"],
        }
        self.cmds = {cmd: func for func, cmds in self.user_commands.items() for cmd in cmds}
        self.last_line = ""

    def handle_command(self, cmd) -> str:
        cmd, *args = cmd.lstrip("/").split(" ")
        if cmd in self.cmds:
            return self.cmds[cmd](args)
        return f"<error>>> unrecognized command={cmd} ({args=})</error>"

    def handle_question(self, user_input: str) -> str:
        question = get_question(user_input)
        msgs = get_msgs(self.instruction, self.chat_history, question, history_size=self.cfg["history_size"])
        answer = get_answer(msgs, model=self.model)
        self.chat_history.extend([question, answer])
        self.last_line = answer["content"]
        return f"<bot>>> {self.last_line}</bot>"

    def input(self, user_input: str):
        print_formatted_text(HTML(f"<user>> {user_input}</user>"), style=self.style)
        if user_input.startswith("/"):
            output = self.handle_command(user_input)
        else:
            output = self.handle_question(user_input)
        if output:
            print_formatted_text(HTML(output), style=self.style)

    def do_config(self, args: list) -> None:
        """Set config values: /config <key=value>"""
        # Print cfg
        if not args:
            return get_formatted_dict(self.cfg)

        # Print cfg with highlighted keys
        kwargs = parse_cfg_kwargs(args)
        if not kwargs:
            return get_formatted_dict(self.cfg, highlight_keys=args)

        # Key validation
        for key, value in kwargs.items():
            if key not in self.cfg:
                return f"<error>>> {key=} not a valid key in cfg:</error>\n{get_formatted_dict(self.cfg)}"
            if key in ["dirs", "files", "style"]:
                return f"<error>>> {key=} can not be set this way, please see {cfg_path}</error>"
            if key == "model":
                if value not in models:
                    return f"<error>>> model='{value}' was not found in models={list(models.keys())}</error>"
                self.model = get_model(model_name=value, env_filename=self.cfg["files"]["env"])
            try:
                if key == "bot":
                    path = f"{self.cfg['dirs']['bots']}/{value}.txt"
                    self.instruction = load_instruction(path=path)
                elif key == "history":
                    path = f"{self.cfg['dirs']['history']}/{value}.txt"
                    self.chat_history = load_history(path=path)
            except FileNotFoundError as e:
                return f"<error>>> could not find a valid file for {key}={value}:\n>> {e}</error>"

            # Update cfg
            self.cfg[key] = value
        return get_formatted_dict(self.cfg, highlight_keys=list(kwargs))

    def do_view_commands(self, _args):
        """View available commands: /commands, /c"""
        output = ""
        for func, cmds in self.user_commands.items():
            output += f"<b>{func.__name__.replace('do_', '').replace('_', ' ')}:</b> /{', /'.join(cmds)}\n"
        return output

    def do_save_message(self, args: list):
        """Save the last message written in console to file: /save <filename>"""
        filename = args[0] if len(args) > 0 else None
        if self.last_line:
            save_msg(self.last_line, path=self.cfg["dirs"]["saved"], filename=filename)
        else:
            return f">> no message to save: {self.last_line=}"

    def do_view_history(self, args: list):
        """Print chat history: /history <i: int>"""
        chat_history = self.chat_history or [{"content": "No chat history"}]
        args = range(len(chat_history)) if len(args) == 0 else args
        output = []
        args = [int(i) for i in args]
        for i in args:
            try:
                output.append(chat_history[i])
            except IndexError:
                return f"<error>>> IndexError: index {i} out of range for {len(chat_history)=}</error>"
        self.last_line = output[-1]["content"]

        # Print history
        args = [i for i in range(len(output))] if len(args) == 0 else args
        for i, msg in zip(args, output):
            i = len(chat_history) + i if i < 0 else i
            print_formatted_text(HTML((f"<b>history[{i}]</b>: {msg['content']}")))

    def do_clear_history(self, _args):
        """Clear chat history: /clear_history, /ch
        NOTE: This does not automatically delete the history file, but the file may be deleted or overwritten on exit
        """
        self.chat_history = []
        print(f">> history cleared: {self.chat_history=}")

    def do_save_history(self, args):
        filename = args[0] if len(args) > 0 else f"{self.cfg['history']}.json"
        save_history(self.chat_history, path=self.cfg["dirs"]["history"], filename=filename)

    def do_quit(self, _args):
        """Quit chat session: /q, /quit, /exit"""
        if self.cfg["save_history_on_exit"] is True:
            save_history(self.chat_history, path=self.cfg["dirs"]["history"], filename=f"{self.cfg['history']}.json")
        if self.cfg["save_config_on_exit"] is True:
            save_cfg(self.cfg)
        exit()
