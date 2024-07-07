import os
import sys
import asyncio
import pyperclip

from dotenv import load_dotenv
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Select, TextArea
from textual.containers import Horizontal
from textual.binding import Binding
from rich.markdown import Markdown

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PATH = os.path.join(ROOT_PATH, "chat/static/")
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "profiles/chat/config.yaml")
sys.path.insert(0, ROOT_PATH)

from src.bot import ChatBot
from src.utils import load_cfg

load_dotenv()


class HistoryBox(TextArea):
    """Displays chat history."""

    BINDINGS = [
        Binding("ctrl+c", "copy", "Copy", key_display="ctrl+C"),
        Binding("ctrl+a", "select_all", "Select all", key_display="ctrl+A"),
    ]

    def on_mount(self) -> None:
        self.read_only = True

    def add_msg(self, msg: str, avatar: str = None):
        if not msg:
            return
        if avatar:
            msg = f"{avatar} {msg}"
        self.text += f"\n{msg}"

    def action_copy(self) -> None:
        pyperclip.copy(self.selected_text)

    def _on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+c":
            pyperclip.copy(self.selected_text)
        elif event.key == "enter":
            self.screen.focus_next()
        else:
            return
        event.prevent_default()


class InputField(TextArea):
    """Input field for the user."""

    BINDINGS = [
        Binding("ctrl+c", "copy", "Copy", key_display="ctrl+C"),
        Binding("ctrl+v", "paste", "Paste", key_display="ctrl+V"),
        Binding("ctrl+x", "cut", "Cut", key_display="ctrl+X"),
        Binding("ctrl+a", "select_all", "Select All", key_display="ctrl+A"),
        Binding("enter", "send", "Send", key_display="Enter"),
        Binding("shift+enter", "newline", "Newline", key_display="shift+Enter"),
    ]

    def on_mount(self) -> None:
        self.styles.height = "4"
        self.tab_behavior = "indent"

    def action_copy(self) -> None:
        pyperclip.copy(self.selected_text)

    def action_paste(self) -> None:
        self.insert(pyperclip.paste())

    def action_newline(self) -> None:
        self.insert("\n")

    def action_cut(self) -> None:
        pyperclip.copy(self.selected_text)
        self.action_delete_left()

    async def action_send(self) -> None:
        question = self.text
        self.text = ""
        await app.handle_messages(question)

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            await self.action_send()
        elif event.key == "escape":
            await app.action_quit()
        else:
            return
        event.prevent_default()


class ChatApp(App):
    CSS_PATH = os.path.join(STATIC_PATH, "styles.css")
    TITLE = "ConsoleBot"
    BINDINGS = [
        Binding("escape", "quit", "Quit", key_display="ESC"),
        Binding("ctrl+c", "", "", key_display=""),  # Prevent ctrl+c from exiting the app
    ]

    def __init__(self, cfg_path: str = None) -> None:
        super().__init__()
        self.cfg = load_cfg(cfg_path=cfg_path)
        self.bot = ChatBot(self.cfg)
        self.greeting = "How can I help you today?"

    def compose(self) -> ComposeResult:
        """Composes the application's root widget"""
        yield Header(id="header")

        # Menu
        with Horizontal(id="menu"):
            yield Select(
                [(key, key) for key in self.bot.chat_models],
                value=self.cfg["model"],
                id="select_model",
                allow_blank=False,
            )
            yield Select(
                [(key, key) for key in self.bot.bots],
                value=self.cfg["bot"],
                id="select_bot",
                allow_blank=False,
            )

        bot_avatar = self.cfg.get("avatars", {}).get("bot")
        yield HistoryBox(f"{bot_avatar} {self.greeting}", id="chat_history")
        yield InputField("", id="input_field")
        yield Footer(id="footer")

    async def on_mount(self) -> None:
        """Triggered when the app is mounted"""
        self.query_one("#input_field", InputField).focus()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Triggered when a Select widget is changed. Get id of the changed widget with `event.select.id`"""
        if event.select.id == "select_model":
            self.cfg["model"] = event.value
        elif event.select.id == "select_bot":
            self.cfg["bot"] = event.value
        self.query_one("#input_field", InputField).focus()

    async def handle_messages(self, question: str) -> None:
        """Asynchronous function that posts user question to chat_history and then gets bot answer"""

        # Question
        user_avatar = self.cfg.get("avatars", {}).get("user")
        chat_history = self.query_one("#chat_history")
        chat_history.add_msg(msg=question, avatar=user_avatar)

        # Wait for user question to be posted before getting answer
        await asyncio.sleep(0.1)

        # Answer
        bot_avatar = self.cfg.get("avatars", {}).get("bot")
        answer = await self.bot.async_chat(question.strip())
        chat_history = self.query_one("#chat_history")
        chat_history.add_msg(msg=answer, avatar=bot_avatar)
        chat_history.scroll_end(animate=False)


if __name__ == "__main__":
    cfg_path = DEFAULT_CONFIG_PATH
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    app = ChatApp(cfg_path=cfg_path)
    app.run()
