import requests

print("Connecting to Ollama...")

url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen3:8b",
    "prompt": "Say hello in one sentence.",
    "stream": False
}

response = requests.post(url, json=data)

print("Response received!")
print(response.json())