import os
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "my-project-0011-490714"
LOCATION = "us-central1"

print(f"Initializing Vertex AI for {PROJECT_ID} in {LOCATION}...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-1.5-flash-001")
print("Generating content...")
try:
    response = model.generate_content("Hello")
    print("Success! Response:", response.text)
except Exception as e:
    print("Error:", str(e))
