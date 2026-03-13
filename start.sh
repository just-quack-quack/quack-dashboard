#!/bin/bash
# Start quack dashboard in tmux

set -e

DASHBOARD_DIR="$HOME/.openclaw/workspace/quack-dashboard"
TMUX_SESSION="main"  # Dashboard runs in main session (binh's desk screen)

# Kill any existing animation/visualization on main session
tmux send-keys -t main C-c
sleep 0.5

# Start dashboard in main session
tmux send-keys -t main "cd $DASHBOARD_DIR && uv run python quack_dashboard.py" Enter

echo "Dashboard started in tmux session: main"
echo "It's now showing on binh's desk screen"
echo "Stop dashboard with: tmux send-keys -t main C-c"
