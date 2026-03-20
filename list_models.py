from google import genai
import os

api_key = os.environ.get("GOOGLE_API_KEY", "AQ.Ab8RN6IwSu4pLl4t3KwfgGe3I6fsWCvXsoTq_dBAH5_x3CbB0Q")
client = genai.Client(api_key=api_key)

print("Available models:")
for m in client.models.list():
    if "flash" in m.name:
        print(m.name)
