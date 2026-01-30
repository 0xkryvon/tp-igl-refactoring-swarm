import os
import sys
from time import time
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


# Patch pour ajouter un délai
original_invoke = llm.invoke

def slow_invoke(*args, **kwargs):
    print("⏳ Waiting 3s to avoid rate limit...")
    time.sleep(3)  # Délai de 3 secondes
    return original_invoke(*args, **kwargs)

llm.invoke = slow_invoke