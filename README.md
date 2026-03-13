# Quack Dashboard

Terminal-based dashboard for binh, powered by Textual.

## About

Quack Dashboard runs in a tmux session and provides real-time updates on:
- Daily research papers from arXiv Robotics
- Active tasks and projects
- System status and information

## Features

- **Extensible**: Easy to add new panels for different data sources
- **Persistent**: Data saved to `data/` directory
- **Heartbeat Updates**: Updates automatically during heartbeat checks
- **Terminal UI**: Fast, keyboard-friendly interface

## Usage

### Starting the Dashboard

```bash
cd ~/.openclaw/workspace/quack-dashboard
./start.sh
```

This runs the dashboard in the `main` tmux session (binh's desk screen).

### Attaching to the Dashboard

The dashboard is visible on binh's desk screen (`main` tmux session). To interact with it directly:

```bash
tmux attach -t main
```

### Stopping the Dashboard

```bash
# Send Ctrl+C to stop the dashboard
tmux send-keys -t main C-c
```

## Heartbeat Integration

During heartbeats, update the dashboard:

```bash
# Update research panel with today's papers
python heartbeat_update.py update-research

# Add a task
python heartbeat_update.py add-task "Working on project X" active

# Update system status
python heartbeat_update.py update-status
```

## Architecture

```
quack-dashboard/
├── quack_dashboard.py      # Main Textual app
├── dashboard_data.py       # Data persistence
├── heartbeat_update.py     # Heartbeat integration
├── start.sh              # Start script
├── data/                 # Saved data
│   ├── papers.json
│   ├── tasks.json
│   └── status.json
└── pyproject.toml        # Project config
```

## Adding New Panels

1. Add new `TabPane` in `quack_dashboard.py`
2. Create data handling in `dashboard_data.py`
3. Update via `heartbeat_update.py`
4. Commit changes

## Requirements

- Python 3.12+
- textual >= 8.0
- tmux
- uv (for package management)

---

Created by: quack quack
Version: 1.0.0
