from dotenv import load_dotenv

from app import ChatApp

load_dotenv()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
