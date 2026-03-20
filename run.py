"""
run.py — Launches the ADK backend (port 8000) and the custom UI server (port 8080) together.
Visit http://localhost:8080 to open the professional UI.
"""
import os
import sys
import subprocess
import threading
import time

# Patch symlink on Windows
original_symlink = getattr(os, "symlink", None)
def mock_symlink(src, dst, *args, **kwargs):
    print(f"Skipping symlink creation: {src} -> {dst}")
os.symlink = mock_symlink


def start_adk_backend():
    """Start the ADK web server on port 8000."""
    from google.adk.cli.cli_tools_click import cli_run
    sys.argv = ["adk", "web", "rag_agent", "--port", "8000"]
    try:
        cli_run()
    except SystemExit as e:
        if e.code != 0:
            raise


def start_ui_server():
    """Start the FastAPI custom UI on port 8080 after a short delay."""
    time.sleep(2)  # Give ADK backend time to start
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, log_level="warning")


if __name__ == "__main__":
    print("=" * 55)
    print("  🧠 Vertex AI RAG Agent — Professional UI")
    print("=" * 55)
    print("  ADK Backend  →  http://localhost:8000")
    print("  Custom UI    →  http://localhost:8080  ← open this")
    print("=" * 55)

    # Launch custom UI server in a background thread
    ui_thread = threading.Thread(target=start_ui_server, daemon=True)
    ui_thread.start()

    # Run ADK backend in the main thread (blocking)
    start_adk_backend()
