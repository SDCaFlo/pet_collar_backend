from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = f"postgresql://{os.getenv("postgres_user")}:{os.getenv("postgres_pass")}" \
    f"@localhost:{os.getenv("postgres_port")}/{os.getenv("postgres_db")}"

settings = Settings()

if __name__ == "__main__":
    print(settings)