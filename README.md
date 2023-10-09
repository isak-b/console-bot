# About chat
ChatGPT in your terminal!

Author: Isak Barbopoulos (isak@xaros.org)

---

<details>
    <summary>Installation</summary><br>

NOTE: You need python, pip and an OpenAI API key to run chat
#### Open root folder in terminal and type:
```bash
pip install .
```

#### Create a file named '.env' in the root of this repo and add the following line:
```bash
OPENAI_API_KEY=<your OpenAI API key here>
```
</details>

<details>
    <summary>Start a new chat</summary><br>

Run `chat/src/__main/__.py` or type the following in your terminal:
```bash
python path/to/chat/src/
```

TIP: Bind the above command to an alias (like 'chat') for easy access

</details>

<details>
    <summary>Commands</summary><br>

Quit:
```
/quit
```

Get a description of a command:
```
/help save
```

Get list of commands and their aliases:
```
/commands
```

Save the last message to disk:
```
/save
```

Print chat history:
```
/history
```

Print a specific message from history:
- NOTE: history counts backwards, so 1=last, 2=second to last, etc
```
/history 2
```

Save a specific message from history:
```
/history 5
/save
```

Change config values:
```
/config prompt=default
```
</details>
