# AutoPilot — The Middleware Killer

An AI agent that watches your screen, learns your patterns, and automates repetitive data transfer tasks.

## What It Does

1. **Observes** — Captures your screen activity (what apps you use, what you copy/paste)
2. **Learns** — Identifies patterns: "Every Monday, copy CRM data to spreadsheet"
3. **Automates** — Executes the repetitive tasks for you
4. **Gets Smarter** — Improves with every interaction

## How to Use

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Start Monitoring
```bash
python monitor.py
```

### Step 3: Check What It Learned
```bash
python dashboard.py
```

### Step 4: Approve Automations
```bash
python approve.py
```

## Architecture

```
┌─────────────────────────────────────────┐
│            AutoPilot Core               │
├─────────────────────────────────────────┤
│  monitor.py    — Screen observation     │
│  learner.py    — Pattern recognition    │
│  automator.py  — Task execution         │
│  dashboard.py  — Web interface          │
│  approve.py    — Human approval         │
└─────────────────────────────────────────┘
```

## How It Works

1. **monitor.py** captures screen every 10 seconds
2. **learner.py** analyzes patterns weekly
3. You review learned patterns in **dashboard.py**
4. You approve patterns → **automator.py** executes them

## Files

| File | Purpose |
|------|---------|
| monitor.py | Captures screen activity |
| learner.py | Learns patterns from activity |
| automator.py | Executes approved automations |
| dashboard.py | Web dashboard to review patterns |
| approve.py | CLI to approve/reject patterns |
| config.py | Configuration settings |
| database.py | SQLite storage |
| requirements.txt | Python dependencies |

## Privacy

- All data stays on YOUR machine
- No cloud upload
- No telemetry
- You control what's monitored
