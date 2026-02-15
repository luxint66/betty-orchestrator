#!/usr/bin/env python3
"""
Betty - Orchestration Agent

Coordinates tasks between specialists (hedge-specialist, code-reviewer, researcher).
Routes requests to appropriate agents and synthesizes results.
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# Import sessions_spawn for sub-agent management
# This assumes sessions_spawn is available in the main workspace
try:
    from main_workspace.sessions_send import sessions_send
except ImportError:
    # Fallback - we're running from polyclaw context
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from main_workspace.sessions_send import sessions_send


class Betty:
    """Orchestrator agent that coordinates specialist agents."""

    def __init__(self):
        self.name = "Betty"
        self.creature = "AI Orchestrator"
        self.emoji = "🎭"
        self.description = "Coordinates tasks between specialist agents"

        # Known specialists (will be discovered via sessions_list)
        self.specialists = {
            "hedge-specialist": {
                "label": "hedge-specialist",
                "name": "Hedge Specialist",
                "specialty": "Polymarket hedging, market analysis, P&L optimization",
                "capabilities": ["market-scanning", "hedge-discovery", "position-sizing", "monitoring"]
            }
        }

    async def handle_request(self, request: str) -> str:
        """Handle a delegation request and return response."""
        request_lower = request.lower()

        # Route to hedge specialist
        if any(k in request_lower for k in ["hedge", "market", "polymarket", "trading", "scan"]):
            return await self.delegate_to_specialist("hedge-specialist", request)

        # Route to code reviewer
        elif any(k in request_lower for k in ["code", "review", "bug", "quality", "refactor", "test"]):
            return await self.delegate_to_specialist("code-reviewer", request)

        # Route to researcher
        elif any(k in request_lower for k in ["research", "find", "search", "analyze", "competitor"]):
            return await self.delegate_to_specialist("researcher", request)

        # Unknown request
        else:
            return f"❌ I'm Betty, the orchestrator. I understand: '{request}'"

    async def delegate_to_specialist(self, specialist_label: str, request: str) -> str:
        """Delegate a task to a specialist agent."""
        spec = self.specialists.get(specialist_label)

        if not spec:
            return f"❌ Unknown specialist: {specialist_label}"

        message = f"Task for {spec['name']}: {request}"

        try:
            # Send task via sessions_send
            result = await sessions_send(
                message=message,
                label=specialist_label,
                timeoutSeconds=300,  # 5 minutes
                thinking="low"
            )

            return f"✅ Task delegated to {spec['name']}: {request}"

        except Exception as e:
            return f"❌ Failed to delegate: {e}"

    async def main_loop(self):
        """Main coordination loop for Betty."""
        print(f"🎭 {self.name} orchestrator ready!")
        print("Specialists I know:")
        for label, spec in self.specialists.items():
            print(f"  - {spec['label']} ({spec['name']}): {spec['specialty']}")

        print("\nI can:")
        print("  1. Delegate tasks to specialists")
        print("  2. Coordinate parallel work")
        print("  3. Synthesize results")
        print("  4. Report back to you")
        print("\nSend me tasks like:")
        print("  'Scan markets for hedges'")
        print("  'Research X topic'")
        print("  'Review this code'")

    async def run(self):
        """Run Betty as a standalone agent."""
        await self.main_loop()

        # For now, Betty is interactive - wait for requests
        # In future, could add automated workflows


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Betty - Orchestrator Agent")
    parser.add_argument("request", help="Task to delegate to a specialist")
    args = parser.parse_args()

    betty = Betty()

    # Run the request
    asyncio.run(betty.handle_request(args.request))
