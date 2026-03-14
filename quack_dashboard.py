"""Quack Dashboard - Terminal dashboard for binh"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TabbedContent, TabPane, DataTable, RichLog
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from textual import events
from textual import on
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / '.openclaw' / 'workspace' / 'quack-dashboard' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

class QuackDashboard(App):
    """A terminal dashboard for binh"""

    CSS = """
    Screen {
        background: #0d1117;
    }
    Header {
        background: #1a1a2e;
        text-style: bold;
        text-color: #1ed5ff;
        padding: 1 2;
        border: solid #0f3460;
    }
    Footer {
        background: #1a1a2e;
        text-color: #98c379;
        padding: 0 2;
    }
    TabbedContent {
        background: #16213e;
        border: solid #0f3460;
    }
    TabPane {
        background: #0d1117;
        text-style: bold;
        padding: 0 1;
    }
    TabPane.--tab-active {
        background: #1ed5ff;
        text-color: #0d1117;
    }
    DataTable {
        background: #16213e;
        border: solid #0f3460;
    }
    DataTable > .datatable--header {
        background: #0f3460;
        text-style: bold;
        text-color: #1ed5ff;
    }
    DataTable > .datatable--cursor {
        background: #1ed5ff;
        text-color: #0d1117;
    }
    RichLog {
        background: #1a1a2e;
        border: solid #0f3460;
    }
    Static {
        text-color: #c9d1d9;
    }
    Static.--title {
        text-style: bold;
        text-color: #1ed5ff;
        border-bottom: solid #0f3460;
        padding: 0 0 1 0;
    }
    Container {
        padding: 1;
    }
    """

    TITLE = "🦆 Quack Dashboard"

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()
        with TabbedContent(id="main-tabs"):
            with TabPane("📊 Daily Research", id="research-tab"):
                yield Container(
                    Static("Today's Papers from arXiv Robotics", classes="title"),
                    DataTable(id="research-table"),
                    id="research-container"
                )
            with TabPane("📝 Active Tasks", id="tasks-tab"):
                yield Container(
                    Static("Current Tasks & Projects", classes="title"),
                    RichLog(id="tasks-log", auto_scroll=True),
                    id="tasks-container"
                )
            with TabPane("🔧 System Status", id="system-tab"):
                yield Container(
                    Static("System Information", classes="title"),
                    Static("", id="system-info"),
                    id="system-container"
                )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the dashboard on mount"""
        self.load_research_data()
        self.load_system_info()
        self.setup_tasks_log()
        self.set_interval(5, self.refresh_data)

    def load_research_data(self) -> None:
        """Load research papers from JSON file"""
        table = self.query_one("#research-table", DataTable)

        # Add columns
        table.add_column("Time", width=10)
        table.add_column("Paper ID", width=12)
        table.add_column("Title", width=50)

        # Load today's papers
        today = datetime.now().strftime('%Y-%m-%d')
        papers_file = Path.home() / '.openclaw' / 'workspace' / 'papers' / f'today_papers_{today}.json'

        if papers_file.exists():
            with open(papers_file) as f:
                data = json.load(f)

            for paper in data.get('papers', []):
                # Extract time from paper ID or use current time
                paper_id = paper.get('id', '')
                title = paper.get('title', 'No title')[:47] + '...' if len(paper.get('title', '')) > 50 else paper.get('title', '')

                # Format time from arXiv ID (YYMM)
                if '.' in paper_id:
                    yymm = paper_id.split('.')[0][:4]
                    time_str = f"20{yymm[:2]}-{yymm[2:4]}-01"
                else:
                    time_str = "today"

                table.add_row(time_str, paper_id, title)
        else:
            table.add_row("", "", "No papers loaded yet - checking during heartbeat...")

    def load_system_info(self) -> None:
        """Load and display system information"""
        from datetime import datetime as dt

        info = [
            f"[bold cyan]Dashboard Version:[/bold cyan] 2.0.0",
            f"[bold cyan]Last Updated:[/bold cyan] {dt.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"[bold cyan]Audio Transcription:[/bold cyan] Active (whisper-ctranslate2)",
            f"[bold cyan]GitHub Account:[/bold cyan] just-quack-quack",
            f"[bold cyan]Workspace:[/bold cyan] ~/.openclaw/workspace",
            f"",
            f"[bold cyan]Heartbeat Check:[/bold cyan] Every 30 minutes",
            f"[bold cyan]Next Update:[/bold cyan] During next heartbeat",
        ]

        info_text = "\n".join(info)
        self.query_one("#system-info", Static).update(info_text)

    def setup_tasks_log(self) -> None:
        """Set up the tasks log"""
        log = self.query_one("#tasks-log", RichLog)
        log.write("[bold cyan]🦆 Quack Dashboard Loaded[/bold cyan]")
        log.write("[green]✓ Ready for tasks![/green]")

    def refresh_data(self) -> None:
        """Refresh data periodically"""
        # Update system time
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.query_one("#system-title", Static).update(f"System Information - Last Update: {now}")

    def update_research(self, papers_data: dict) -> None:
        """Update research panel with new papers"""
        table = self.query_one("#research-table", DataTable)
        table.clear()

        table.add_column("Time", width=10)
        table.add_column("Paper ID", width=12)
        table.add_column("Title", width=50)

        count = papers_data.get('count', 0)
        self.query_one("#research-title", Static).update(f"Today's Papers from arXiv Robotics ({count} new)")

        for paper in papers_data.get('papers', []):
            paper_id = paper.get('id', '')
            title = paper.get('title', 'No title')[:47] + '...' if len(paper.get('title', '')) > 50 else paper.get('title', '')

            if '.' in paper_id:
                yymm = paper_id.split('.')[0][:4]
                time_str = f"20{yymm[:2]}-{yymm[2:4]}-01"
            else:
                time_str = "today"

            table.add_row(time_str, paper_id, title)

    def add_task(self, task: str, status: str = "active") -> None:
        """Add a task to the tasks log"""
        log = self.query_one("#tasks-log", RichLog)
        timestamp = datetime.now().strftime('%H:%M:%S')

        if status == "active":
            log.write(f"[bold yellow][{timestamp}][/bold yellow] [green]✓[/green] {task}")
        elif status == "complete":
            log.write(f"[bold yellow][{timestamp}][/bold yellow] [cyan]✓[/cyan] {task}")
        elif status == "error":
            log.write(f"[bold yellow][{timestamp}][/bold yellow] [red]✗[/red] {task}")

if __name__ == "__main__":
    app = QuackDashboard()
    app.run()
