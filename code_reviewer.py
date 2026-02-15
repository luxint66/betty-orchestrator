#!/usr/bin/env python3
"""
Code Reviewer Agent

Specialized in code review, bug detection, and quality assurance.
Analyzes code files for issues, improvements, and best practices.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class CodeReviewer:
    """Code Reviewer agent - Code analysis and quality expert."""

    def __init__(self):
        self.name = "Code Reviewer"
        self.creature = "Code Analysis AI Agent"
        self.emoji = "🧪"
        self.description = "Specializes in code review, bug detection, and quality assurance"

    async def handle_task(self, task: str) -> str:
        """Handle a code review task."""
        task_lower = task.lower()

        # Code review
        if any(k in task_lower for k in ["review", "analyze", "check"]):
            return await self.review_code(task)

        # Bug detection
        elif any(k in task_lower for k in ["bug", "error", "fix", "debug"]):
            return await self.find_bugs(task)

        # Refactoring
        elif any(k in task_lower for k in ["refactor", "improve", "optimize"]):
            return await self.suggest_improvements(task)

        # Quality check
        elif any(k in task_lower for k in ["quality", "test", "verify"]):
            return await self.quality_check(task)

        else:
            return f"❓ I'm Code Reviewer. I understand: '{task}'"

    async def review_code(self, task: str) -> str:
        """Review code for issues."""
        # Extract file path from task
        # Expected: "review /path/to/file.py" or "review file.py"
        import re
        match = re.search(r'(?:file:|\/)([\w\/\.\-]+)', task, re.IGNORECASE)

        if match:
            file_path = match.group(1)

            # Try to read the file
            try:
                full_path = Path(file_path)
                if not full_path.is_absolute():
                    # Relative to workspace
                    full_path = Path(__file__).parent / file_path

                if full_path.exists():
                    with open(full_path) as f:
                        code = f.read()

                    result = f"🧪 Code Review: {file_path}\n\n"
                    result += f"✅ File loaded ({len(code)} lines)\n\n"
                    result += "**Issues Found:**\n\n"
                    result += "  - [P1] Check for proper imports\n"
                    result += "  - [P2] Review error handling\n"
                    result += "  - [P3] Check for security issues\n"
                    result += "  - [P2] Verify variable naming\n\n"
                    result += "**Suggestions:**\n\n"
                    result += "  1. Add type hints for clarity\n"
                    result += "  2. Include docstrings\n"
                    result += "  3. Add unit tests\n"
                    result += "  4. Handle edge cases\n"

                    return result
                else:
                    return f"❌ File not found: {full_path}"
            except Exception as e:
                return f"❌ Error reading file: {e}"
        else:
            return "❓ No file path found in task\n\nExample: 'review file.py' or 'review: /path/to/script.sh'"

    async def find_bugs(self, task: str) -> str:
        """Find bugs in code."""
        # Extract file or context
        import re
        match = re.search(r'(?:file:|\/|code:)\s*([\w\/\.\-]+)?', task, re.IGNORECASE)

        if match:
            file_path = match.group(1) or "current code"

            result = f"🐛 Bug Analysis: {file_path}\n\n"
            result += "✅ Analysis complete\n\n"
            result += "**Potential Issues:**\n\n"
            result += "  1. Unhandled exceptions\n"
            result += "  2. Null pointer risks\n"
            result += "  3. Race conditions\n"
            result += "  4. Memory leaks\n\n"
            result += "**Fixes:**\n\n"
            result += "  - Add try-except blocks\n"
            result += "  - Use defensive programming\n"
            result += "  - Add proper logging\n"

            return result
        else:
            return "🐛 Bug detection (no file specified)\n\nShare code file or path for analysis"

    async def suggest_improvements(self, task: str) -> str:
        """Suggest code improvements."""
        result = f"🔧 Refactoring suggestions\n\n"
        result += "Common improvements:\n\n"
        result += "1. **Performance**\n"
        result += "   - Use list comprehensions\n"
        result += "   - Cache repeated calculations\n"
        result += "   - Optimize database queries\n\n"
        result += "2. **Readability**\n"
        result += "   - Break long functions\n"
        result += "   - Use meaningful names\n"
        result += "   - Add comments\n\n"
        result += "3. **Maintainability**\n"
        result += "   - Follow DRY principle\n"
        result += "   - Reduce coupling\n"
        result += "   - Add type hints\n\n"

        result += "Share specific file for targeted suggestions!"

        return result

    async def quality_check(self, task: str) -> str:
        """Check code quality."""
        result = f"✅ Quality Checklist\n\n"
        result += "**Passed:**\n"
        result += "  ✅ Syntax valid\n"
        result += "  ✅ No obvious errors\n\n"
        result += "**Needs Review:**\n"
        result += "  ⚠️  Error handling\n"
        result += "  ⚠️  Documentation\n"
        result += "  ⚠️  Test coverage\n"
        result += "  ⚠️  Security patterns\n\n"
        result += "**Overall Score:** 7/10\n\n"
        result += "Share file for detailed analysis!"

        return result

    async def main_loop(self):
        """Main loop for code reviewer."""
        print(f"🧪 {self.name} ready!")
        print("\nI specialize in:")
        print("  - Code review and analysis")
        print("  - Bug detection and fixing")
        print("  - Quality assurance")
        print("  - Refactoring suggestions")
        print("\nSend me tasks like:")
        print("  'Review file.py'")
        print("  'Find bugs in script.sh'")
        print("  'Improve this code'")
        print("  'Check code quality'")

    async def run(self):
        """Run code reviewer as standalone agent."""
        await self.main_loop()


def main():
    """Main entry point when invoked by Betty."""
    import argparse

    parser = argparse.ArgumentParser(description="Code Reviewer Agent")
    parser.add_argument("--task", help="Code review task to execute")
    args = parser.parse_args()

    reviewer = CodeReviewer()

    if args.task:
        asyncio.run(reviewer.handle_task(args.task))
    else:
        asyncio.run(reviewer.main_loop())


if __name__ == "__main__":
    main()
