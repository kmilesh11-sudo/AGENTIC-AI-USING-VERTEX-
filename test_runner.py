"""
Test the ADK agent programmatic runner (InMemoryRunner pattern).

Runs the agent with a simple test message and prints the response.
Usage:
    python test_runner.py
    python test_runner.py "what corpora are available?"
"""

import asyncio
import sys

from rag_agent.runner import run_agent


async def main():
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "list available corpora"
    print(f"[test_runner] Testing agent with: {message!r}")
    response = await run_agent(message, session_id="test-session")
    if response:
        print(f"\n[test_runner] Agent responded successfully ({len(response)} chars).")
    else:
        print("\n[test_runner] WARNING: Agent returned an empty response.")


if __name__ == "__main__":
    asyncio.run(main())
