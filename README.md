# About
ChatGPT in your terminal!

Author: Isak Barbopoulos (isak@xaros.org)

# Install chat
NOTE: You need python, pip and an OpenAI API key before you can install chat
#### Open root folder in terminal and type:
```bash
pip install .
```

# Setup
#### Create a file named '.env' in the root of this repo and add the following line:
```bash
OPENAI_API_KEY=<your OpenAI API key here>
```

# Start chat
NOTE: Bind this to an alias (like 'chat') for easy access
```bash
python path/to/src/
```

# Chat commands

Quit:
```
/quit
```

Get command description:
```
/help save
```

Get list of commands and their aliases:
```
/commands
```

Save last line:
```
/save
```

Print chat_history:
```
/history
```

Print specific message in chat_history:
```
/history 2
```

Save a specific message from chat_history:
```
/history 5
/save
```

Change config values:
```
/config prompt=default
```

