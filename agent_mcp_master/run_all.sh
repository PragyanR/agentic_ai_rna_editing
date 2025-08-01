#!/bin/bash
./run_mcp_server.sh
./run_orchestrator.sh
./run_planner.sh
./run_crispr_cas13.sh


## Run Inspector Backend
COMMAND_TO_RUN="cd /Users/praggu/Documents/CRISPR_research/agent/agentic_ai_rna_editing/agent_mcp_master/inspector/backend && ./run_backend_cmd.sh"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF

## Run Inspector Frontend
COMMAND_TO_RUN="cd /Users/praggu/Documents/CRISPR_research/agent/agentic_ai_rna_editing/agent_mcp_master/inspector/frontend && ./run_frontend_cmd.sh"
osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF