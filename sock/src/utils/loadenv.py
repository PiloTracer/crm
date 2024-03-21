from dotenv import load_dotenv
import os

# Function to load .env and get the value of a key
def get_env_value(key: str) -> str:
    load_dotenv()  # Load .env file
    return os.getenv(key)

