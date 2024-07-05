import asyncio
import random
import textwrap
import shutil
from halo import Halo

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Input, Button, Static, Select, Label
from textual.containers import ScrollableContainer, Horizontal
from textual.binding import Binding

from config import load_cfg
from bot import ChatBot

spinner_msgs = [
    "Simulating a progress bar...",
    "Blink twice if you see errors... Just kidding, don't blink.",
    "Calculating the meaning of life... might take a while.",
    "Sure, let me just google that for you...",
    "Hold tight, butter-bot is on a coffee break...",
    "Converting nonsense into somewhat more understandable nonsense...",
    "Attempting to give a damn... but failing... Loading anyway.",
    "Oh look at the dancing pixels on the screen",
    "Writing down the answer on a piece of paper...",
    "Patience, young padawan. I'm faster than your ex texting back!",
    "If this takes too long, blame it on the wifi or the squirrels.",
    "Busy doing science-y stuff... not that you'd understand.",
    "I'll be ready in a jiffy! Or a jiffy and a half. Who's counting?",
    "Hold on, I'm just feeding my hamster.",
    "Generating more loading messages...",
    "Re-reading the question again...",
    "Let me guess, you're in a hurry? Tough luck, kid!",
    "Can't rush genius... or loading bars for that matter.",
    "Like trying to explain quantum physics to a toddler.",
    "Please wait while I pretend to load something for you...",
    "I'm on it. Unlike you, I'm actually good at multitasking!",
    "Just a second... or five... Just wait it out, alright?",
    "It would probably be faster if you just google'd it, just saying...",
    "Wait, you asked what?",
]


class UserMessageBox(Widget):
    """Message boxes for user questions"""

    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.text, classes=f"message {self.role}")


class BotMessageBox(Widget):
    """Message boxes for bot answers"""

    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.text, classes=f"message {self.role}")


class Chat(App):
    CSS_PATH = "static/styles.css"
    TITLE = "Chat"
    BINDINGS = [
        Binding("escape", "quit", "Quit", key_display="ESC"),
        Binding("ctrl+x", "clear", "Clear", key_display="ctrl+X"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.cfg = load_cfg()
        self.bot = ChatBot(self.cfg)
        self.greeting = "How can I help you today?"
        self.question_template = f"{self.cfg['avatars']['user']} {{question}}"
        self.answer_template = f"{self.cfg['avatars']['bot']} {{answer}}"

    def compose(self) -> ComposeResult:
        """Composes the application's root widget"""
        yield Label(id="info")

        # Menu
        with Horizontal(id="menu_box"):
            yield Select(
                [(key, key) for key in self.bot.models],
                value=self.cfg["model"],
                prompt="select model",
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
            yield BotMessageBox(self.answer_template.format(answer=self.greeting), role="answer")

        # User input
        with Horizontal(id="input_box"):
            yield Input(id="user_input")

            # NOTE: send_button is currently disabled
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
        terminal_width, _ = shutil.get_terminal_size()
        terminal_width *= 0.8

        # User question
        user_input = self.query_one("#user_input", Input)
        self.toggle_widgets(user_input, send_button)
        self.query_one("#user_input", Input).focus()
        question = user_input.value
        question = textwrap.fill(question, width=terminal_width)
        message_box = UserMessageBox(self.question_template.format(question=question), "question")
        history_box.mount(message_box)
        history_box.scroll_end(animate=False)
        with user_input.prevent(Input.Changed):
            user_input.value = ""

        # Wait for user question to be posted before getting bot answer
        await asyncio.sleep(0.1)

        # Bot answer
        # NOTE: Display spinner while waiting for response
        spinner = Halo(text=random.choice(spinner_msgs), spinner="dots")
        spinner.start()
        answer = await self.bot.async_get_response(message_box.text)
        spinner.stop()
        answer = textwrap.fill(answer, width=terminal_width)
        history_box.mount(BotMessageBox(self.answer_template.format(answer=answer), "answer"))

        self.toggle_widgets(user_input, send_button)
        history_box.scroll_end(animate=False)

    def toggle_widgets(self, *widgets: Widget) -> None:
        for w in widgets:
            w.disabled = not w.disabled
