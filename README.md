# ConsoleBot
Chat with ChatGPT in your terminal!

ConsoleBot is a Command Line Interface (CLI) built with the Python package [textual](https://textual.textualize.io/) that allows you to chat with ChatGPT in your terminal.

**Author**: Isak Barbopoulos (isak@xaros.org)

---

<details>
    <summary>Installation</summary>

1. Make sure you have Python >=3.9 and an OpenAI API key.

2. Open your terminal of choice and clone this repo:
```bash
git clone https://github.com/isak-b/console-bot.git
```

3. Install the package and its dependencies:
```bash
cd console-bot
pip install .
```

4. Create a file named '.env' in the console-bot folder and add the following line:
```bash
OPENAI_API_KEY=<your OpenAI API key here>
```

</details>

<details>
    <summary>Usage</summary>
Open a terminal in the console-bot folder, and then either:

1. Open an interactive chat interface in your terminal by writing:

```bash
python chat
```

2. Or get an answer to a single question directly in the terminal:

```bash
python ask "How do I recursively find and delete all .log files in a directory using the terminal?"
```

TIP: Bind "python chat" and "python ask" to aliases in e.g., `~/.bashrc` (if you use bash) or `~/.zshrc` (if you use zshell) for easy access. For example:
```bash
alias chat="python path/to/console-bot/chat/"
alias ask="python path/to/console-bot/ask/"
```

Then just type `chat` or `ask "<your question>"` from any location in your terminal.

See more details on how to install and make modifications below.

</details>

<details>
    <summary>Customize existing profiles and assistants</summary>

The default profiles are found here:
- Chat: `console-bot/profiles/chat/`
- Ask: `console-bot/profiles/ask/`

Modify existing profiles and assistants:
- To change the config of one of the default profiles, open `config.yaml` in either `console-bot/profiles/chat/` or `console-bot/profiles/ask/`
- Change the values you wish to modify, e.g., `model: gpt-4-turbo`
- To modify an existing bot, open the .txt file of the bot you want to modify in the `assistants/` directory, and write your own instructions

</details>

<details>
    <summary>Create new assistants</summary>

Create new assistants:
- Open the `assistants/` folder in the profile folder that you wish to add a bot to
- Create a new .txt file with your custom instructions
- If you for example save your new instructions as `console-bot/profiles/chat/assistants/NewBot.txt`, then "NewBot" will appear as a choice in the chat interface.
- You can select which bot is loaded as default by opening `config.yaml` and setting `bot: NewBot`.
- Note that since the ask interface isn't interactive, you must set the bot according to the above step in `profiles/ask/config.yaml`.

</details>

<details>
    <summary>Create new profiles</summary>

Create entirely new profiles:
- Create a new folder in `console-bot/profiles/`
- Add a `config.yaml` file with the settings you wish to use.
- Add a `assistants/` directory with the assistants that you wish to include.
- Then, to use the new profile, call either the chat or ask command with the path to your `config.yaml` as an argument, e.g.,:

```bash
python chat "path/to/profiles/my-profile/config.yaml"
python ask "Some question" "path/to/profiles/my-profile/config.yaml"
```

</details>

<details>
    <summary>Todo</summary>

Some of the things I might implement soon:

- Make it so users can save and manage chat history (create, name and select history_ids at will)

- Add support for other LLMs

- Add image generation (not currently supported by textual)

</details>
