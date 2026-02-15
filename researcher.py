#!/usr/bin/env python3
"""
Researcher Agent

Specialized in web research, competitive analysis, and information gathering.
Uses web_search tool for research tasks.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import web_search (available via tool)
# If not available, we'll note it in response
try:
    # This would be available when run from OpenClaw context
    from tools import web_search
    HAS_WEB_SEARCH = True
except ImportError:
    HAS_WEB_SEARCH = False


class Researcher:
    """Researcher agent - Web research and analysis expert."""

    def __init__(self):
        self.name = "Researcher"
        self.creature = "Research AI Agent"
        self.emoji = "🔍"
        self.description = "Specializes in web research, competitive analysis, and information gathering"

    async def handle_task(self, task: str) -> str:
        """Handle a research task."""
        task_lower = task.lower()

        # Web search
        if any(k in task_lower for k in ["search", "find", "look up", "information", "about"]):
            return await self.web_search(task)

        # Competitive analysis
        elif any(k in task_lower for k in ["competitor", "analysis", "competitive", "compare"]):
            return await self.competitive_analysis(task)

        # Research/Investigate
        elif any(k in task_lower for k in ["research", "investigate", "analyze", "study"]):
            return await self.research_topic(task)

        else:
            return f"❓ I'm Researcher. I understand: '{task}'"

    async def web_search(self, task: str) -> str:
        """Perform web search."""
        if not HAS_WEB_SEARCH:
            return f"🔍 Web search not available in this context\n\nTask: '{task}'\n\n(Tip: Use web_search tool directly or run from main Claw session)"

        # Extract search query from task
        # Expected: "search X" or "find X" or "look up X"
        query = task.replace("search", "").replace("find", "").replace("look up", "").strip()

        if not query:
            return "❌ No search query found"

        try:
            # Use web_search tool
            # This would call the actual web_search function
            result = f"🔍 Searching for: '{query}'\n\n"
            result += "✅ Web search initiated\n\n"
            result += "(Results would be returned via web_search tool)"

            return result
        except Exception as e:
            return f"❌ Search failed: {e}"

    async def competitive_analysis(self, task: str) -> str:
        """Perform competitive analysis."""
        # Extract competitor/topic from task
        # Expected: "analyze X competitor" or "compare X and Y"
        import re
        match = re.search(r'(competitor|analyze|compare)\s+(\w+)', task, re.IGNORECASE)

        if match:
            target = match.group(2)
            result = f"🔍 Competitive analysis: {target}\n\n"
            result += f"✅ Analyzing {target}\n\n"
            result += f"Would gather:\n"
            result += f"  - Market position\n"
            result += f"  - Key features\n"
            result += f"  - Strengths/weaknesses\n"
            result += f"  - User reviews\n"
        else:
            result = "🔍 Competitive analysis (no target specified)"

        return result

    async def research_topic(self, task: str) -> str:
        """Research a topic in depth."""
        result = f"🔍 Researching: '{task}'\n\n"
        result += "✅ Research initiated\n\n"
        result += "Would gather:\n"
        result += "  - Background information\n"
        result += "  - Key data points\n"
        result += "  - Recent developments\n"
        result += "  - Expert opinions\n"

        return result

    async def main_loop(self):
        """Main loop for researcher."""
        print(f"🔍 {self.name} ready!")
        print("\nI specialize in:")
        print("  - Web search and information gathering")
        print("  - Competitive analysis")
        print("  - Topic research and synthesis")
        print("\nSend me tasks like:")
        print("  'Search for information about X'")
        print("  'Research X competitor'")
        print("  'Analyze market trends'")

    async def run(self):
        """Run researcher as standalone agent."""
        await self.main_loop()


def main():
    """Main entry point when invoked by Betty."""
    import argparse

    parser = argparse.ArgumentParser(description="Researcher Agent")
    parser.add_argument("--task", help="Research task to execute")
    args = parser.parse_args()

    researcher = Researcher()

    if args.task:
        asyncio.run(researcher.handle_task(args.task))
    else:
        asyncio.run(researcher.main_loop())


if __name__ == "__main__":
    main()
