import os
import json
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

from bot import ChatBot
from config import load_cfg, save_cfg, get_formatted_cfg

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

style = {
    "user": "",
    "bot": "#00ADB2",
    "error": "ansired",
}


class Chat:
    def __init__(self, cfg: dict = load_cfg()):
        self.intro = "Entering chat session - see commands: '/commands'"
        self.bot = ChatBot(cfg=cfg)
        self.style = Style.from_dict(style)
        self.user_prefix = ">"
        self.bot_prefix = ">>"
        self.input_buffer = ""
        self.response = ""

        # user_commands = {func: ["alias1", "alias2"]}
        self.user_commands = {
            self.do_view_commands: ["commands", "cmds", "c"],
            self.do_set_config: ["config", "cfg"],
            self.do_save_message: ["save", "s"],
            self.do_view_history: ["history", "hs"],
            self.do_save_history: ["save_history", "save_hs"],
            self.do_clear_history: ["clear_history", "clear_hs"],
            self.do_quit: ["quit", "q", "exit"],
        }
        # cmds = {"alias1": func, "alias2": func}
        self.cmds = {cmd: func for func, cmds in self.user_commands.items() for cmd in cmds}

    def paste(self, user_input: str):
        """Adds pasted user_input to input_buffer"""
        user_input = user_input.replace("<", "&lt;").replace(">", "&gt;")
        self.input_buffer += user_input
        print_formatted_text(HTML(f"<user>{self.user_prefix}\n{user_input}</user>".rstrip("\n")), style=self.style)

    def enter(self, user_input: str):
        """Adds user_input to input_buffer and sends it"""
        user_input = user_input.replace("<", "&lt;").replace(">", "&gt;")
        self.input_buffer += user_input
        print_formatted_text(HTML(f"<user>{self.user_prefix} {user_input}</user>"), style=self.style)

        # Check if command
        if self.input_buffer.startswith("/"):
            self.response = self.handle_command(self.input_buffer)
        else:
            self.response = self.bot.get_response(self.input_buffer).replace("<", "&lt;").replace(">", "&gt;")
            self.response = f"<bot>{self.bot_prefix} {self.response}</bot>"
        print_formatted_text(HTML(self.response), style=self.style)

        # Clear input_buffer
        self.input_buffer = ""

    def handle_command(self, cmd) -> str:
        cmd, *args = cmd.lstrip("/").split(" ")
        if cmd in self.cmds:
            return self.cmds[cmd](args)
        return f"<error>unrecognized command={cmd} ({args=})</error>"

    def do_view_commands(self, _args):
        """View available commands: /commands, /c"""
        output = ""
        width = max([len(c) for c in list(self.cmds)])
        for func, cmds in self.user_commands.items():
            name = func.__name__.replace("do_", "").replace("_", " ")
            output += f"<b>{name:{width}}</b> : /{', /'.join(cmds)}\n"
        return output

    def do_set_config(self, args: list) -> None:
        """Set config values: /config key=value"""
        options = {
            "model": list(self.bot.models),
            "bot": list(self.bot.bots),
            "save_config_on_exit": ["true", "false"],
            "save_history_on_exit": ["true", "false"],
        }
        kwargs = {arg.split("=")[0]: arg.split("=")[1] for arg in args if "=" in arg}
        for key, val in kwargs.items():
            if key in ["dirs", "paths"]:
                return f"<error>{key=} must be changed by editing the cfg file directly</error>"
            if key in options and val not in options[key]:
                return f"<error>'{val}' is not valid, use one of: {options[key]}</error>"
            if isinstance(self.bot.cfg[key], bool):
                val = val.lower() == "true"
            elif isinstance(self.bot.cfg[key], int):
                val = int(val)
            self.bot.cfg[key] = val
            args.append(key)

        # Print cfg
        if not args:
            return get_formatted_cfg(self.bot.cfg, options=options)
        return get_formatted_cfg(self.bot.cfg, options=options, highlight_keys=args)

    def do_save_message(self, args: list) -> None:
        """Save the last message written in console to file: /save <filename>"""
        if not self.response:
            return f">> no response to save: {self.response=}"
        filename = args[0] if len(args) > 0 else None
        path = self.bot.cfg["dirs"]["saved"]

        if not filename:
            files = os.listdir(ROOT_PATH + path)
            max_num = 0
            for file in files:
                if file.startswith("output_"):
                    try:
                        num = int(file.split("_")[1].split(".")[0])
                    except ValueError:
                        continue
                    max_num = max(num, max_num)
            new_num = max_num + 1
            filename = f"output_{str(new_num).zfill(3)}.txt"

        output_path = f"{ROOT_PATH}{path}{filename}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(self.response)
        return f"saved message:\n  {self.response=}\n  {output_path=}"

    def do_view_history(self, args: list):
        """Print chat history: /history <i: int>"""
        chat_history = self.bot.chat_history or [{"content": "No chat history"}]
        args = range(len(chat_history)) if len(args) == 0 else args
        msgs = []
        args = [int(i) for i in args]
        for i in args:
            try:
                msgs.append(chat_history[i])
            except IndexError:
                return f"<error>IndexError: index {i} out of range for {len(chat_history)=}</error>"
        self.response = msgs[-1]["content"]

        # Print history
        args = [i for i in range(len(msgs))] if len(args) == 0 else args
        output = ""
        for i, msg in zip(args, msgs):
            i = len(chat_history) + i if i < 0 else i
            output += f"<b>history[{i}]</b>: {msg['content']}\n"
        return output

    def do_clear_history(self, _args):
        """Clear chat history: /clear_history, /ch"""
        self.bot.chat_history = []
        return f"history cleared: {self.bot.chat_history=}"

    def do_save_history(self, args: list = []):
        """Save chat history to file"""
        history = self.bot.chat_history
        path = ROOT_PATH + self.bot.cfg["dirs"]["history"]
        filename = args[0] if len(args) > 0 else f"{self.bot.cfg['history']}.json"
        output_path = f"{path}{filename}"
        if history:
            with open(output_path, "w") as f:
                json.dump(history, f)
                return f"history saved: {output_path}"
        return f"no history to save, delete file manually if you want it removed: {output_path}"

    def do_quit(self, _args):
        """Quit chat session: /q, /quit, /exit"""
        if self.bot.cfg["save_history_on_exit"] is True:
            self.do_save_history()
        if self.bot.cfg["save_config_on_exit"] is True:
            save_cfg(self.bot.cfg)
        exit()

    def start(self):
        """Start chat session"""
        print(self.intro)
        kb = KeyBindings()
        terminal_history = InMemoryHistory()

        @kb.add(Keys.Enter)
        def _(event):
            user_input = event.current_buffer.document.text
            event.current_buffer.document = event.current_buffer.document.__class__()
            self.enter(user_input)

        @kb.add(Keys.BracketedPaste)
        def _(event):
            user_input = "\n".join(event.data.split("\r"))
            self.paste(user_input)

        with patch_stdout():
            while True:
                prompt(
                    f"{self.user_prefix} ",
                    key_bindings=kb,
                    history=terminal_history,
                    auto_suggest=AutoSuggestFromHistory(),
                )
