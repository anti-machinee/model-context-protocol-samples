import os
from dotenv import load_dotenv

load_dotenv()


class Configuration:
    conninfo = os.getenv("DATABASE_URL")


configs = Configuration()