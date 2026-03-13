#!/bin/bash
# Start quack dashboard in tmux

set -e

DASHBOARD_DIR="$HOME/.openclaw/workspace/quack-dashboard"
TMUX_SESSION="dashboard"

# Check if tmux session exists
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "Dashboard session already exists. Attach with: tmux attach -t $TMUX_SESSION"
    exit 0
fi

# Create new tmux session with dashboard
tmux new-session -d -s "$TMUX_SESSION" -c "$DASHBOARD_DIR"

# Start the dashboard
tmux send-keys -t "$TMUX_SESSION" "uv run python quack_dashboard.py" Enter

echo "Dashboard started in tmux session: $TMUX_SESSION"
echo "Attach with: tmux attach -t $TMUX_SESSION"
echo "Kill with: tmux kill-session -t $TMUX_SESSION"
