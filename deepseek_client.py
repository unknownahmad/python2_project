import os
import requests
from dotenv import load_dotenv

load_dotenv("private.env")  # Load API key from environment file.

API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Stores the DeepSeek API key.


def get_fun_fact():
    """Fetches a short AI-generated football fun fact from the DeepSeek API."""
    if not API_KEY:
        return "No API key found."

    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Give me a short fun football fact."}
        ],
        "max_tokens": 50
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"AI Error: {response.status_code}"

        res_json = response.json()
        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"
