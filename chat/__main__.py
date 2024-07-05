import sys
from dotenv import load_dotenv

from app import ChatApp

load_dotenv()


if __name__ == "__main__":
    cfg_path = None
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    app = ChatApp(cfg_path=cfg_path)
    app.run()
