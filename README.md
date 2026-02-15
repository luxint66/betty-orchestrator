# Betty Orchestrator

Multi-agent orchestration system with specialist delegates.

## Components

- `betty.py` - Main orchestrator
- `betty_orchestrator.py` - Orchestration logic
- `betty_config.json` - Personality config

## Specialists

- `hedge_specialist.py` - Hedge trading specialist
- `researcher.py` - Research specialist
- `code_reviewer.py` - Code review specialist

## Supporting Tools

- `check_hedges.py` - Hedge position checker
- `hedge_status_report.py` - Status reporting
- `cron_*.sh` - Cron job scripts

## Usage

```
betty, scan markets
betty, research X
betty, review file.py
```
