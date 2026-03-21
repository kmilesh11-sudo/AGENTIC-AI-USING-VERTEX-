import os
import sys

original_symlink = getattr(os, "symlink", None)
def mock_symlink(src, dst, *args, **kwargs):
    print(f"Skipping symlink creation: {src} -> {dst}")
os.symlink = mock_symlink

import subprocess

if __name__ == "__main__":
    print("Starting ADK Web Server on port 8091...")
    subprocess.run([sys.executable, "-m", "google.adk.cli", "web", ".", "--port", "8091"])

