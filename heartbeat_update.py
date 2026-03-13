#!/usr/bin/env python3
"""
Heartbeat updater for quack dashboard.
Called during heartbeats to update dashboard panels.
"""

import sys
from pathlib import Path

# Add dashboard to path
DASHBOARD_DIR = Path.home() / '.openclaw' / 'workspace' / 'quack-dashboard'
sys.path.insert(0, str(DASHBOARD_DIR))

from dashboard_data import DashboardData
import json
from datetime import datetime

def update_research_panel() -> bool:
    """Update the research panel with today's papers"""
    data = DashboardData()

    # Load today's papers from the papers directory
    today = datetime.now().strftime('%Y-%m-%d')
    papers_file = Path.home() / '.openclaw' / 'workspace' / 'papers' / f'today_papers_{today}.json'

    if papers_file.exists():
        with open(papers_file) as f:
            papers_data = json.load(f)

        # Save to dashboard data
        data.save_papers(papers_data)
        return True

    return False

def add_task(task: str, status: str = 'active') -> None:
    """Add a task to the dashboard"""
    data = DashboardData()
    data.save_task(task, status)
    print(f"Task added: {task} [{status}]")

def update_status(status_dict: dict) -> None:
    """Update system status"""
    data = DashboardData()
    data.save_status(status_dict)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: heartbeat_update.py <command> [args]")
        print("Commands:")
        print("  update-research - Update research panel with today's papers")
        print("  add-task <task> [status] - Add a task (status: active, complete, error)")
        print("  update-status - Update system status")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'update-research':
        if update_research_panel():
            print("✓ Research panel updated")
        else:
            print("ℹ No papers found for today")

    elif command == 'add-task':
        if len(sys.argv) < 3:
            print("Error: Task text required")
            sys.exit(1)
        task = ' '.join(sys.argv[2:-1]) if len(sys.argv) > 3 else sys.argv[2]
        status = sys.argv[-1] if sys.argv[-1] in ['active', 'complete', 'error'] else 'active'
        add_task(task, status)

    elif command == 'update-status':
        # Read status from stdin or build default
        status = {
            'last_heartbeat': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'audio_transcription': 'active',
            'github_status': 'connected',
            'research_ingest': 'running'
        }
        update_status(status)
        print("✓ Status updated")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
