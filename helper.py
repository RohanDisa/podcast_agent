import os
from dotenv import load_dotenv


def load_env() -> None:
    if os.path.exists(".env"):
        load_dotenv()




