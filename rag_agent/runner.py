"""
ADK Programmatic Runner for the Vertex AI RAG Agent.

This module implements the ADK-documented pattern for running agents
programmatically using InMemoryRunner, as described at:
https://google.github.io/adk-docs/get-started/python/#run-your-agent

Usage:
    python -m rag_agent.runner
    or import run_agent() for use in scripts.
"""

import asyncio
import os
import sys

# Patch os.symlink on Windows to avoid errors in ADK internals
_original_symlink = getattr(os, "symlink", None)
os.symlink = lambda src, dst, *a, **kw: None

from dotenv import load_dotenv

# Load from the .env inside the rag_agent package directory
_env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(_env_path)

from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types

from rag_agent.agent import root_agent


async def run_agent(user_message: str, session_id: str = "default-session") -> str:
    """
    Run the RAG agent with a user message and return the final text response.

    Args:
        user_message: The message to send to the agent.
        session_id: A session identifier for conversation state.

    Returns:
        The agent's final text response as a string.
    """
    runner = InMemoryRunner(agent=root_agent, app_name="rag_agent")
    session = runner.session_service.create_session(
        app_name="rag_agent",
        user_id="user",
        session_id=session_id,
    )

    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=user_message)],
    )

    final_response = ""
    print(f"\n[Runner] Sending message: {user_message!r}")
    print("-" * 60)

    async for event in runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=content,
    ):
        # Print streaming text chunks as they arrive
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)
                    final_response += part.text

    print("\n" + "-" * 60)
    return final_response


if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "list available corpora"
    asyncio.run(run_agent(message))
