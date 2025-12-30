import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Please add it to your .env file."
    )
