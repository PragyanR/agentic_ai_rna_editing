#!/bin/bash
COMMAND_TO_RUN="cd /Users/praggu/Documents/CRISPR_research/agent/agentic_ai_rna_editing/agent_mcp_master && uv run --env-file .env src/a2a_mcp/agents/ --agent-card agent_cards/planner_agent.json --port 10102"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF