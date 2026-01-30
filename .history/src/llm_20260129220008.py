import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    print("❌ CRITICAL ERROR: GOOGLE_API_KEY missing in .env")
    sys.exit(1)

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash", 
    temperature=0,
    transport="rest"
)