./run_mcp_server.sh
./run_orchestrator.sh
./run_planner.sh
./run_crispr_cas13.sh


## Run Inspector Backend
COMMAND_TO_RUN="cd /Users/rathamma/Documents/code_workspace/a2a_mcp/inspector/backend && ./run_backend_cmd.sh"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF

## Run Inspector Frontend
COMMAND_TO_RUN="cd /Users/rathamma/Documents/code_workspace/a2a_mcp/inspector/frontend && ./run_frontend_cmd.sh"
osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF