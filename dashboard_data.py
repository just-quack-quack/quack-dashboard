"""Data persistence for quack dashboard"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

DATA_DIR = Path.home() / '.openclaw' / 'workspace' / 'quack-dashboard' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

class DashboardData:
    """Manage dashboard data persistence"""

    def __init__(self):
        self.papers_file = DATA_DIR / 'papers.json'
        self.tasks_file = DATA_DIR / 'tasks.json'
        self.status_file = DATA_DIR / 'status.json'

    def save_papers(self, papers_data: Dict[str, Any]) -> None:
        """Save research papers data"""
        with open(self.papers_file, 'w') as f:
            json.dump(papers_data, f, indent=2)

    def load_papers(self) -> Dict[str, Any]:
        """Load research papers data"""
        if self.papers_file.exists():
            with open(self.papers_file) as f:
                return json.load(f)
        return {'count': 0, 'papers': [], 'date': None}

    def save_task(self, task: str, status: str = 'active') -> None:
        """Save a task to the task log"""
        tasks = []
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                tasks = json.load(f)

        task_entry = {
            'task': task,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }

        tasks.append(task_entry)

        # Keep only last 100 tasks
        if len(tasks) > 100:
            tasks = tasks[-100:]

        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)

    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the task log"""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                return json.load(f)
        return []

    def save_status(self, status_data: Dict[str, Any]) -> None:
        """Save system status data"""
        status_data['last_updated'] = datetime.now().isoformat()
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)

    def load_status(self) -> Dict[str, Any]:
        """Load system status data"""
        if self.status_file.exists():
            with open(self.status_file) as f:
                return json.load(f)
        return {}

    def clear_papers(self) -> None:
        """Clear papers data for new day"""
        self.save_papers({'count': 0, 'papers': [], 'date': datetime.now().strftime('%Y-%m-%d')})
