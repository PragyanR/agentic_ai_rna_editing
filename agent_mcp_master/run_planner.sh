
COMMAND_TO_RUN="cd /Users/rathamma/Documents/code_workspace/a2a_mcp  && source .venv/bin/activate && uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/planner_agent.json --port 10102"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF