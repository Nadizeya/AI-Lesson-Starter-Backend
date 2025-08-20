import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

def make_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")  # optional

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")

    # Python SDK expects api_key
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)

def model_id():
    return os.getenv("OPENAI_MODEL", "gpt-5")
