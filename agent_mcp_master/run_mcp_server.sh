#!/bin/bash

# Command to execute in the new Terminal window
COMMAND_TO_RUN="cd /Users/praggu/Documents/CRISPR_research/agent/agentic_ai_rna_editing/agent_mcp_master && source .venv/bin/activate && uv run  --env-file .env src/a2a_mcp/mcp/ --run mcp-server --transport sse"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF

