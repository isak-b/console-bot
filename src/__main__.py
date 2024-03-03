from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout

from bot import ChatBot


def chat():
    intro = "Entering chat session - try: '/help', '/commands', '/config', '/quit'"
    prompt_prefix = "> "
    kb = KeyBindings()
    bot = ChatBot()

    @kb.add("enter")
    def _(event):
        user_input = event.current_buffer.document.text.strip()
        event.current_buffer.document = event.current_buffer.document.__class__()
        bot.input(user_input)

    print(intro)
    with patch_stdout():
        while True:
            prompt(prompt_prefix, key_bindings=kb, multiline=True)


if __name__ == "__main__":
    chat()
