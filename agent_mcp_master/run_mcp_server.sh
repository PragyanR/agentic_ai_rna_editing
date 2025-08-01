#uv venv # (if not already done)
#source .venv/bin/activate
# Runs on port 10000 by default, change as needed by setting the --host and --port parameters.
#!/bin/bash

# Command to execute in the new Terminal window
COMMAND_TO_RUN="cd /Users/rathamma/Documents/code_workspace/a2a_mcp && source .venv/bin/activate && uv run  --env-file .env src/a2a_mcp/mcp/ --run mcp-server --transport sse"

osascript <<EOF
tell application "Terminal"
    do script "${COMMAND_TO_RUN}"
    activate
end tell
EOF

