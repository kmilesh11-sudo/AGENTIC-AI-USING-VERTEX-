"""Test if Vertex AI RAG API is accessible (listing corpora, independent of LLM model)."""
import os
import sys
from pathlib import Path

# Load .env from rag_agent directory
from dotenv import load_dotenv
_env_path = Path(__file__).parent / "rag_agent" / ".env"
load_dotenv(_env_path)

import vertexai

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

if not PROJECT_ID:
    print("[ERROR] GOOGLE_CLOUD_PROJECT is not set. Check rag_agent/.env")
    sys.exit(1)

print(f"Initializing Vertex AI with project={PROJECT_ID}, location={LOCATION} ...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

print("Testing RAG API (list_corpora)...")
try:
    from vertexai import rag
    corpora = list(rag.list_corpora())
    print("[OK] RAG list_corpora worked. Found %d corpora." % len(corpora))
    for c in corpora:
        print("  - %s (%s)" % (c.display_name, c.name))
except Exception as e:
    print("[FAIL] RAG list_corpora: %s" % str(e)[:300])
    sys.exit(1)
