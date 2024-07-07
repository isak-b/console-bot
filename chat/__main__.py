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

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PATH = os.path.join(ROOT_PATH, "chat/static/")
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "profiles/chat/config.yaml")
sys.path.insert(0, ROOT_PATH)

from src.bot import ChatBot
from src.utils import load_cfg

load_dotenv()


class SelectBox(Select):
    BINDINGS = [
        Binding("enter", "show_overlay", "Show items", key_display="Enter"),
    ]

    def _on_key(self, event: events.Key) -> None:
        if event.key == "up" and self.expanded is False:
            if self.screen.focus_chain[0] != self:  # Stop at element 0
                self.screen.focus_previous()
        elif event.key == "down" and self.expanded is False:
            self.screen.focus_next()
        elif event.key == "left":
            self.screen.focus_previous()
        elif event.key == "right":
            self.screen.focus_next()
        else:
            return
        event.prevent_default()


class HistoryBox(TextArea):
    """Displays chat history."""

    BINDINGS = [
        Binding("ctrl+c", "copy", "Copy", key_display="ctrl+C"),
        Binding("ctrl+a", "select_all", "Select all", key_display="ctrl+A"),
        Binding("PgUp", "cursor_page_up", "Page up", show=True),
        Binding("PgDown", "cursor_page_down", "Page down", show=True),
    ]

    async def on_mount(self) -> None:
        self.read_only = True
        self.language = "markdown"

    async def add_msg(self, msg: str, avatar: str = None):
        if avatar:
            msg = f"{avatar} {msg}"
        if len(self.text) > 0:
            msg = f"\n\n{msg}"
        self.text += msg
        self.action_cursor_page_down()
        self.action_cursor_line_end()

    def action_copy(self) -> None:
        pyperclip.copy(self.selected_text)

    def _on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+c":
            pyperclip.copy(self.selected_text)
        elif event.key == "enter":
            self.screen.focus_next()
        elif event.key == "up":
            if self.cursor_location == (0, 0):
                self.screen.focus_previous()
            else:
                self.action_cursor_up()
        elif event.key == "down":
            if self.cursor_at_end_of_text:
                self.screen.focus_next()
            else:
                self.action_cursor_down()
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
        Binding("shift+enter", "newline", "Newline", key_display="Shift+Enter"),
    ]

    def on_mount(self) -> None:
        self.styles.height = "4"
        self.tab_behavior = "indent"
        self.language = "markdown"

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
        if self.text:
            await self.app.handle_messages()

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            await self.action_send()
        elif event.key == "escape":
            await app.action_quit()
        elif event.key == "up":
            if self.cursor_location == (0, 0):
                self.screen.focus_previous()
            else:
                self.action_cursor_up()
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
            yield SelectBox(
                [(key, key) for key in self.bot.chat_models],
                value=self.cfg["model"],
                id="select_model",
                allow_blank=False,
            )
            yield SelectBox(
                [(key, key) for key in self.bot.bots],
                value=self.cfg["bot"],
                id="select_bot",
                allow_blank=False,
            )

        yield HistoryBox(id="chat_history")
        yield InputField(id="input_field")
        yield Footer(id="footer")

    async def on_mount(self) -> None:
        """Triggered when the app is mounted"""
        bot_avatar = self.cfg.get("avatars", {}).get("bot")
        chat_history = self.query_one("#chat_history", HistoryBox)
        await chat_history.add_msg(self.greeting, avatar=bot_avatar)
        self.query_one("#input_field", InputField).focus()

    def on_select_changed(self, event: SelectBox.Changed) -> None:
        """Triggered when a SelectBox widget is changed. Get id of the changed widget with `event.select.id`"""
        if event.select.id == "select_model":
            self.cfg["model"] = event.value
        elif event.select.id == "select_bot":
            self.cfg["bot"] = event.value
        self.query_one("#input_field", InputField).focus()

    async def handle_messages(self) -> None:
        """Asynchronous function that posts user question to chat_history and then gets bot answer"""
        input_field = self.query_one("#input_field", InputField)
        question = input_field.text
        input_field.text = ""

        # Question
        chat_history = self.query_one("#chat_history", HistoryBox)
        user_avatar = self.cfg.get("avatars", {}).get("user")
        await chat_history.add_msg(msg=question, avatar=user_avatar)
        chat_history.scroll_end(animate=False)
        await asyncio.sleep(0.1)  # Wait for the message to be added before sending the next message

        # Answer
        bot_avatar = self.cfg.get("avatars", {}).get("bot")
        answer = await self.bot.async_chat(question.strip())
        await chat_history.add_msg(msg=answer, avatar=bot_avatar)
        chat_history.scroll_end(animate=False)


if __name__ == "__main__":
    cfg_path = DEFAULT_CONFIG_PATH
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    app = ChatApp(cfg_path=cfg_path)
    app.run()
