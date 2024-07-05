# About chat
Chat with ChatGPT in your terminal!

This is a Command Line Interface (CLI) that allows you to chat with ChatGPT in your terminal. It is built on the [textual](https://textual.textualize.io/) library and provides a simple and interactive way to access models like gpt-3.5-turbo, gpt-4-turbo and gpt-4o.

Author: Isak Barbopoulos (isak@xaros.org)

---

<details>
    <summary>Installation</summary><br>

#### 1. Make sure you have python >=3.9 and an OpenAI API key.

#### 2. Then open this folder in a terminal and type:
```bash
pip install .
```

#### 3. Create a file named '.env' in this folder and add the following line:
```bash
OPENAI_API_KEY=<your OpenAI API key here>
```
</details>

<details>
    <summary>Start a new chat</summary><br>

cd into this folder with your terminal of choice and type: 

```bash
python src
```

TIP: Bind the command to an alias (like 'chat') and store it in .bashrc or .zshrc for easy access. E.g.,:

```bash
alias chat='python ~/path/to/chat/src'
```

</details>

<details>
    <summary>Create your own assistants</summary><br>

Write instructions in a .txt file and save it in `chat/bots/` and it will become automatically available as a bot.

</details>


<details>
    <summary>Todo</summary><br>

- Make it so users can save chat history again (and let them create, name and select history_ids at will)

- Add support for other LLMs

- Add image generation (not currently supported by textual)

</details>
