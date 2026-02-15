#!/usr/bin/env python3
"""
Betty - Orchestrator Agent (Sub-Agent Version)

Coordinates tasks between specialists (hedge-specialist, code-reviewer, researcher).
Invoked by Claw when user says "Betty, <task>".
"""

import json
import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent))

# Configuration
BETTY_CONFIG = Path(__file__).parent / "betty_config.json"
HEDGE_TEST_SCRIPT = "/home/luxinterior/.openclaw/workspace/hedge_test"

class Betty:
    """Orchestrator that routes tasks to specialists."""

    def __init__(self):
        self.load_config()

    def load_config(self):
        """Load personality and routing config."""
        if BETTY_CONFIG.exists():
            try:
                with open(BETTY_CONFIG) as f:
                    config = json.load(f)
                    self.name = config["name"]
                    self.emoji = config["emoji"]
                    self.tone = config["tone"]
                    self.acknowledgments = config["acknowledgments"]
                    self.specialists = config["specialists"]
                    self.examples = config["examples"]
            except Exception as e:
                print(f"⚠️  Could not load Betty config: {e}")
                self.fallback_config()
        else:
            print("⚠️  Betty config not found, using defaults")
            self.fallback_config()

    def fallback_config(self):
        """Fallback config if file not found."""
        self.name = "Betty"
        self.emoji = "🎭"
        self.acknowledgments = {
            "routing": "🎭 Routing...",
            "delegated": "✅ Task delegated",
            "complete": "✅ Complete",
            "error": "❌ Error",
            "unknown": "❓ Not sure what you mean"
        }
        self.specialists = {
            "hedge-specialist": {
                "name": "Hedge Specialist",
                "keywords": ["hedge", "market", "polymarket", "trading", "scan"],
            },
            "researcher": {
                "name": "Researcher",
                "keywords": ["research", "find", "search", "analyze", "competitor"],
            },
            "code-reviewer": {
                "name": "Code Reviewer",
                "keywords": ["code", "review", "bug", "quality", "refactor", "test"],
            }
        }

    def route_task(self, task: str) -> tuple[str, str]:
        """Route task to appropriate specialist.
        Returns: (specialist_name, response)
        """
        task_lower = task.lower()

        # Route to hedge specialist
        for label, spec in self.specialists.items():
            if any(keyword in task_lower for keyword in spec["keywords"]):
                return spec["name"], f"{self.emoji} {self.acknowledgments['routing']} {spec['name']}"

        # Unknown
        return None, f"{self.emoji} {self.acknowledgments['unknown']}"

    def execute_task(self, task: str) -> str:
        """Execute a task by delegating to appropriate specialist."""
        task_lower = task.lower()

        # Hedge-related tasks
        if any(k in task_lower for k in ["scan", "hedge", "market", "trading", "polymarket"]):
            import subprocess

            # Parse for scan limit
            import re
            limit_match = re.search(r'(\d+)', task)
            limit = limit_match.group(1) if limit_match else "20"

            try:
                result = subprocess.run(
                    [HEDGE_TEST_SCRIPT, "scan", "--limit", limit],
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                if result.returncode == 0:
                    return f"✅ Scan complete!\n\n{result.stdout[-500:]}"
                else:
                    return f"❌ Scan failed:\n{result.stderr}"
            except Exception as e:
                return f"❌ Error: {e}"

        # Research tasks
        elif any(k in task_lower for k in ["research", "find", "search", "investigate", "competitor"]):
            import subprocess
            try:
                researcher_path = Path(__file__).parent / "researcher.py"
                result = subprocess.run(
                    ["python3", str(researcher_path), "--task", task],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return result.stdout
            except Exception as e:
                return f"❌ Research error: {e}"

        # Code review tasks
        elif any(k in task_lower for k in ["code", "review", "bug", "quality", "debug", "fix"]):
            import subprocess
            try:
                reviewer_path = Path(__file__).parent / "code_reviewer.py"
                result = subprocess.run(
                    ["python3", str(reviewer_path), "--task", task],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return result.stdout
            except Exception as e:
                return f"❌ Code review error: {e}"

        return f"{self.emoji} Task received: '{task}'\n\nRouting..."

    def show_help(self) -> str:
        """Show Betty's capabilities."""
        msg = f"{self.emoji} **{self.name} - Orchestrator**\n\n"
        msg += f"**Specialists:**\n"

        for label, spec in self.specialists.items():
            msg += f"\n{self.emoji} **{spec['name']}**\n"
            msg += f"   Keywords: {', '.join(spec['keywords'][:5])}\n"

        msg += f"\n**Examples:**\n"
        for example in self.examples[:4]:
            msg += f"   • `Betty, {example}`\n"

        return msg


def main():
    """Main entry point when invoked by Claw."""
    import argparse

    parser = argparse.ArgumentParser(description="Betty - Orchestrator Agent")
    parser.add_argument("--task", help="Task to orchestrate")
    args = parser.parse_args()

    betty = Betty()

    if args.task:
        # Route and execute
        specialist, routing_msg = betty.route_task(args.task)
        response = betty.execute_task(args.task)

        print(f"{routing_msg}\n{response}")
    else:
        # Show help
        print(betty.show_help())


if __name__ == "__main__":
    main()
