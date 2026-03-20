"""
Vertex AI RAG Agent

A package for interacting with Google Cloud Vertex AI RAG capabilities.
"""

import os
import vertexai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Vertex AI configuration from environment
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")

# Initialize Vertex AI at package load time
try:
    if PROJECT_ID and LOCATION:
        print(f"Initializing Vertex AI with project={PROJECT_ID}, location={LOCATION}")
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("Vertex AI initialization successful")
    else:
        print(
            f"Missing Vertex AI configuration. PROJECT_ID={PROJECT_ID}, LOCATION={LOCATION}. "
            f"Tools requiring Vertex AI may not work properly."
        )
except Exception as e:
    print(f"Failed to initialize Vertex AI: {str(e)}")
    print("Please check your Google Cloud credentials and project settings.")

# ADK discovers root_agent via: importlib.import_module("rag_agent").agent.root_agent
# So we must expose the 'agent' submodule as an attribute of this package.
from . import agent  # noqa: E402

__all__ = ["agent"]
