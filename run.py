import os
import sys

original_symlink = getattr(os, "symlink", None)
def mock_symlink(src, dst, *args, **kwargs):
    print(f"Skipping symlink creation: {src} -> {dst}")
os.symlink = mock_symlink

from google.adk.cli.cli_tools_click import cli_run

if __name__ == "__main__":
    sys.argv = ["adk", "web", "rag_agent"]
    try:
        cli_run()
    except SystemExit as e:
        if e.code != 0:
            raise
