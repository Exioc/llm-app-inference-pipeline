import requests
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL

#https://ollama.com/library

url = f"{OLLAMA_BASE_URL}/api/pull"

headers = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "command-r-plus:104b",
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)
