import os
import sys
import asyncio
import yaml
import random

from dotenv import load_dotenv
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Header, Footer, Input, Button, Select, Static
from textual.containers import ScrollableContainer, Horizontal
from textual.binding import Binding
from rich.markdown import Markdown
from halo import Halo

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PATH = os.path.join(ROOT_PATH, "chat/static/")
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "profiles/chat/config.yaml")
sys.path.insert(0, ROOT_PATH)

from src.bot import ChatBot
from src.utils import load_cfg

load_dotenv()


class MessageBox(Widget):
    """A message box for a question or answer"""

    def __init__(self, text: str, role: str, avatar: str = None) -> None:
        self.text = text
        self.role = role
        self.avatar = avatar
        super().__init__()

    def compose(self) -> ComposeResult:
        if self.avatar:
            self.text = f"{self.avatar} {self.text}"
            self.text = self.text.replace(f"{self.avatar} `", f"{self.avatar}\n`")
        yield Static(Markdown(self.text), shrink=True, classes=self.role)


class UserMessageBox(MessageBox): ...


class BotMessageBox(MessageBox): ...


class ChatApp(App):
    CSS_PATH = os.path.join(STATIC_PATH, "styles.css")
    SPINNER_PATH = os.path.join(STATIC_PATH, "spinner.yaml")
    TITLE = "ConsoleBot"
    BINDINGS = [
        Binding("escape", "quit", "Quit", key_display="ESC"),
        Binding("ctrl+x", "clear", "Clear", key_display="ctrl+X"),
    ]

    def __init__(self, cfg_path: str = None) -> None:
        super().__init__()
        self.cfg = load_cfg(cfg_path=cfg_path)
        self.bot = ChatBot(self.cfg)
        self.greeting = "How can I help you today?"
        with open(self.SPINNER_PATH, "r") as f:
            self.spinner_msgs = yaml.safe_load(f)

    def compose(self) -> ComposeResult:
        """Composes the application's root widget"""
        yield Header()

        # Menu
        with Horizontal(id="menu_box"):
            yield Select(
                [(key, key) for key in self.bot.chat_models],
                value=self.cfg["model"],
                prompt="select chat model",
                id="select_model",
            )
            yield Select(
                [(key, key) for key in self.bot.bots],
                value=self.cfg["bot"],
                prompt="select bot",
                id="select_bot",
            )

        # History box
        with ScrollableContainer(id="history_box"):
            avatar = self.cfg.get("avatars", {}).get("bot")
            yield BotMessageBox(self.greeting, role="answer", avatar=avatar)

        # User input
        with Horizontal(id="input_box"):
            yield Input(id="user_input")

            # NOTE: send_button is currently disabled and hidden
            yield Button(label="", variant="default", id="send_button", disabled=True)

        yield Footer()

    async def on_mount(self) -> None:
        """Triggered when the app is mounted"""
        self.query_one("#user_input", Input).focus()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Triggered when a Select widget is changed. Get id of the changed widget with `event.select.id`"""
        if event.select.id == "select_model":
            self.cfg["model"] = event.value
        elif event.select.id == "select_bot":
            self.cfg["bot"] = event.value

    def action_clear(self) -> None:
        """Triggered when the clear command is entered. Clears history box and creates new bot instance."""
        self.bot = ChatBot(self.cfg)
        history_box = self.query_one("#history_box")
        history_box.remove()
        self.mount(ScrollableContainer(id="history_box"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Triggered when a Button is pressed. Get id with: `event.button.id`"""
        if event.button.id == "send_button":
            # NOTE: send_button is currently disabled and hidden
            await self.handle_messages()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Triggered when Input is submitted. Get id with: `event.input.id`"""
        if event.input.id == "user_input":
            await self.handle_messages()

    async def handle_messages(self) -> None:
        """Handles and displays user questions and bot responses"""
        send_button = self.query_one("#send_button")
        history_box = self.query_one("#history_box")

        # User question
        user_input = self.query_one("#user_input", Input)
        self.toggle_widgets(user_input, send_button)
        self.query_one("#user_input", Input).focus()
        question = user_input.value
        avatar = self.cfg.get("avatars", {}).get("user")
        message_box = UserMessageBox(question, role="question", avatar=avatar)
        history_box.mount(message_box)
        history_box.scroll_end(animate=False)
        with user_input.prevent(Input.Changed):
            user_input.value = ""

        # Wait for user question to be posted before getting bot answer
        await asyncio.sleep(0.1)

        # Bot answer
        # NOTE: Display spinner while waiting for response
        spinner = Halo(text=random.choice(self.spinner_msgs), spinner="dots")
        spinner.start()
        answer = await self.bot.async_chat(question.strip())
        spinner.stop()
        avatar = self.cfg.get("avatars", {}).get("bot")
        history_box.mount(BotMessageBox(answer, role="answer", avatar=avatar))

        self.toggle_widgets(user_input, send_button)
        history_box.scroll_end(animate=False)

    def toggle_widgets(self, *widgets: Widget) -> None:
        for w in widgets:
            w.disabled = not w.disabled


if __name__ == "__main__":
    cfg_path = DEFAULT_CONFIG_PATH
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    app = ChatApp(cfg_path=cfg_path)
    app.run()
