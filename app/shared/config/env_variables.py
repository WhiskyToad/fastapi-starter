import os
from dotenv import load_dotenv


load_dotenv()


DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
SECRET_KEY = os.environ.get("JWT_SECRET", "")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "")
