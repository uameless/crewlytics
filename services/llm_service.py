import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Create Gemini model (flash model is recommended for fast agents)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_llm_response(prompt: str) -> str:

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in Gemini call: {e}")
        return "LLM call failed."
