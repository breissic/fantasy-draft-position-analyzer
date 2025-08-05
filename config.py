import os
from dotenv import load_dotenv

def getKey():
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    return GEMINI_API_KEY
