import os
import sys
import asyncio
import pyperclip

from dotenv import load_dotenv
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Select, TextArea, TabbedContent, TabPane, OptionList
from textual.widgets.option_list import Option, Separator
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_PATH = os.path.join(ROOT_PATH, "chat/static/")
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "profiles/chat/config.yaml")
sys.path.insert(0, ROOT_PATH)

from src.bot import ChatBot
from src.utils import load_cfg, get_time_separator

load_dotenv()

navigation_map = {
    "history_list": {"up": "menu", "right": "chat_history"},
    "chat_history": {"left": "history_list", "up": "menu", "down": "input_field"},
    "input_field": {"left": "history_list", "up": "chat_history"},
    "menu": {
        "down": {"tab_chat": "history_list", "tab_assistant": "select_assistant", "tab_settings": "select_model"},
    },
}


class Menu(TabbedContent):
    def on_mount(self):
        self.focused_tab = "foo bar"

    def _on_key(self, event: events.Key) -> None:
        if event.key == "down":
            if self.active != self.focused_tab:
                target = self.app.query_one(f"#{navigation_map[self.id][event.key][self.active]}")
                target.focus()
            else:
                return
        else:
            return
        event.prevent_default()

    def on_tab_pane_focused(self):
        self.focused_tab = self.active


class SelectBox(Select): ...


class HistoryList(OptionList):
    def _on_key(self, event: events.Key) -> None:
        if event.key == "up":
            if self.highlighted is None or self.highlighted > 0:
                self.action_cursor_up()
                self.action_select()
        elif event.key == "right":
            target = self.app.query_one(f"#{navigation_map[self.id][event.key]}")
            target.focus()
            target.cursor_location = (0, 0)
        elif event.key == "down":
            if self.highlighted is None or self.highlighted < self.option_count - 1:
                self.action_cursor_down()
                self.action_select()
        else:
            return
        event.prevent_default()


class ChatHistory(TextArea):
    """Displays chat history."""

    BINDINGS = [
        Binding("ctrl+c", "copy", "Copy", key_display="ctrl+C"),
        Binding("ctrl+a", "select_all", "Select all", key_display="ctrl+A"),
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
        if event.key == "left":
            if self.cursor_location == (0, 0):
                self.app.query_one(f"#{navigation_map[self.id][event.key]}").focus()
            else:
                self.action_cursor_left()
        elif event.key == "up":
            if self.cursor_location == (0, 0):
                self.app.query_one(f"#{navigation_map[self.id][event.key]}").focus()
            else:
                self.action_cursor_up()
        elif event.key == "down":
            if self.cursor_at_end_of_text:
                self.app.query_one(f"#{navigation_map[self.id][event.key]}").focus()
            else:
                self.action_cursor_down()
        elif event.key == "enter":
            self.screen.focus_next()
        elif event.key == "ctrl+c":
            pyperclip.copy(self.selected_text)
        else:
            return
        event.prevent_default()


class InputField(TextArea):
    """Input field for the user."""

    BINDINGS = [
        Binding("ctrl+c", "copy", "Copy", key_display="ctrl+C"),
        Binding("ctrl+v", "paste", "Paste", key_display="ctrl+V"),
        Binding("ctrl+x", "cut", "Cut", key_display="ctrl+X"),
        Binding("ctrl+a", "select_all", "Select all", key_display="ctrl+A"),
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
                self.app.query_one(f"#{navigation_map[self.id][event.key]}").focus()
            else:
                self.action_cursor_up()
        elif event.key == "left":
            if self.cursor_location == (0, 0):
                self.app.query_one(f"#{navigation_map[self.id][event.key]}").focus()
            else:
                self.action_cursor_left()
        elif event.key == "down":
            if not self.cursor_at_end_of_text:
                self.action_cursor_down()
        else:
            return
        event.prevent_default()


class ChatApp(App):
    CSS_PATH = os.path.join(STATIC_PATH, "styles.css")
    TITLE = "ConsoleBot"
    BINDINGS = [
        Binding("escape", "quit", "Quit", key_display="ESC"),
        Binding("ctrl+c", "", "", key_display=""),  # Prevent ctrl+c from exiting the app
        Binding("ctrl+s", "save", "Save", key_display="ctrl+S"),
    ]

    def __init__(self, cfg_path: str = None) -> None:
        super().__init__()
        self.greeting = "How can I help you today?"
        self.bot = ChatBot(load_cfg(cfg_path=cfg_path))
        self.bot.add_new_chat()
        self.avatars = self.bot.cfg.get("avatars", {})

    def compose(self) -> ComposeResult:
        """Create widgets for the app"""
        yield Header(id="header")
        with Menu(id="menu"):
            with TabPane("Chat", id="tab_chat"):
                with Horizontal():
                    yield HistoryList(id="history_list")
                    with Vertical():
                        yield ChatHistory(id="chat_history")
                        yield InputField(id="input_field")
            with TabPane("Assistant", id="tab_assistant"):
                with Vertical():
                    yield SelectBox(
                        [(key, key) for key in self.bot.assistants],
                        value=self.bot.cfg["assistant"],
                        id="select_assistant",
                        allow_blank=False,
                    )
            with TabPane("Settings", id="tab_settings"):
                with Vertical():
                    yield SelectBox(
                        [(key, key) for key in self.bot.models["chat"]],
                        value=self.bot.cfg["models"]["chat"],
                        id="select_model",
                        allow_blank=False,
                    )

        yield Footer(id="footer")

    async def on_mount(self) -> None:
        """Triggered when the app is first mounted"""
        await self.set_history_list()
        self.query_one("#input_field", InputField).focus()
        self.query_one("#menu").active = "tab_settings"

    def on_select_changed(self, event: SelectBox.Changed) -> None:
        """Triggered when a SelectBox widget is changed. Get id of the changed widget with `event.select.id`"""
        if event.select.id == "select_model":
            self.bot.cfg["models"]["chat"] = event.value
        elif event.select.id == "select_assistant":
            self.bot.cfg["assistant"] = event.value

    async def on_option_list_option_selected(self, event: HistoryList.OptionSelected) -> None:
        """Triggered when an HistoryList widget is changed."""
        history_id = event.option.prompt
        await self.set_history(history_id=history_id)

    async def action_save(self) -> None:
        self.bot.save_messages()

    async def set_history_list(self):
        history_list = self.query_one("#history_list", HistoryList)
        history_list.clear_options()

        # Add options
        options, separators = [], []
        for i, history_id in enumerate(self.bot.history_ids):
            if i == 1:
                options.append(Separator())

            # Add separators based on date
            if i > 0:
                date = self.bot._history[history_id]["date"]
                time_separator = get_time_separator(date)

                if time_separator not in separators:
                    options.append(Option(f"{time_separator}:", disabled=True))
                    separators.append(time_separator)

            options.append(Option(history_id))
        history_list.add_options(options)

        # Select option
        selected_option = [opt.prompt for opt in history_list._options].index(self.bot.history_id)
        history_list.highlighted = selected_option
        await self.set_history(history_id=self.bot.history_id)

    async def set_history(self, history_id: str = None) -> None:
        self.bot.history_id = history_id
        chat_history = self.query_one("#chat_history", ChatHistory)
        chat_history.text = ""
        for msg in self.bot.history:
            if msg["role"] != "system":
                await chat_history.add_msg(msg=msg["content"], avatar=self.avatars.get(msg["role"]))

    async def handle_messages(self) -> None:
        """Asynchronous function that posts user question to chat_history and then gets bot answer"""
        input_field = self.query_one("#input_field", InputField)
        question = input_field.text
        input_field.text = ""

        # Question
        chat_history = self.query_one("#chat_history", ChatHistory)
        user_avatar = self.bot.cfg.get("avatars", {}).get("user")
        await chat_history.add_msg(msg=question, avatar=user_avatar)
        chat_history.scroll_end(animate=False)
        await asyncio.sleep(0.1)  # Wait for the message to be added before sending the next message

        # Answer
        bot_avatar = self.bot.cfg.get("avatars", {}).get("assistant")
        answer = await self.bot.async_chat(question.strip())
        await chat_history.add_msg(msg=answer, avatar=bot_avatar)
        chat_history.scroll_end(animate=False)

        # Rename and update history_id
        await self.bot.rename_history_id(msg={"role": "user", "content": question})
        await self.set_history_list()


if __name__ == "__main__":
    cfg_path = DEFAULT_CONFIG_PATH
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    app = ChatApp(cfg_path=cfg_path)
    app.run()
