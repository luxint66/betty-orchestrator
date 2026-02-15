# BETTY.md - Betty Orchestrator

## What is Betty?

Betty is an orchestrator agent that coordinates task delegation to specialist agents:
- 📊 **Hedge Specialist** — Polymarket hedging, market analysis
- 🔍 **Researcher** — Research, search, analysis
- 🧪 **Code Reviewer** — Code review, bug fixes

## How to Invoke Betty

**Pattern:** "Betty, <task>"

```
Betty, scan markets for hedges
Betty, research Polymarket competitors
Betty, review my trading bot code
Betty, find hedges with 95% coverage
```

**Claw (me) detects this pattern and spawns Betty automatically.**

## How Betty Works

1. **User says:** "Betty, scan markets for hedges"
2. **Claw detects:** Pattern match "Betty, X"
3. **Claw spawns:** Betty as sub-agent via `sessions_spawn`
4. **Betty routes:** Analyzes task → picks Hedge Specialist
5. **Specialist executes:** Runs hedge scan script
6. **Betty synthesizes:** Returns formatted result
7. **Claw delivers:** Response back to user

## What Betty Can Do

**Hedge Trading:**
```
Betty, scan top 20 markets
Betty, monitor active hedges
Betty, check hedge status
Betty, find hedges with 0.95 coverage
```

**Research:**
```
Betty, research X competitor
Betty, analyze market trends
Betty, find information about Y
```

**Code:**
```
Betty, review this code
Betty, check for bugs in script.py
Betty, refactor this function
```

## Betty's Personality

Configured in: `/home/luxinterior/.openclaw/workspace/betty_config.json`

Current settings:
- Name: Betty
- Emoji: 🎭
- Tone: Efficient but warm
- Response: Concise with details on request

Edit `betty_config.json` to change her personality!

## Files

- `betty.py` — Orchestrator agent executable
- `betty_config.json` — Personality & routing config
- `betty_orchestrator.py` — Legacy version (keep for reference)

## When NOT to Use Betty

Use **Claw** (me) directly for:
- Quick questions
- Brainstorming
- "What do you think?" discussions
- File operations
- Debugging help
- General assistance

Use **Betty** for:
- Task management
- Hedge operations
- Research projects
- Code reviews
- Multi-step workflows

---

_Betty is your task orchestrator. Claw is your sounding board. 🦞🎭_
