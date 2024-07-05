from dotenv import load_dotenv

from chat import Chat

load_dotenv()


if __name__ == "__main__":
    app = Chat()
    app.run()
