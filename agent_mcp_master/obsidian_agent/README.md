Step 1: Create an .env file in agent root directory (obsidian_agent)
.env should have the following:
OPENAI_API_KEY="Replace with your key"

Step 2: Ensure your Obsidian MCP Server is up and running. This will be in obsidian_mcp_server

Step 3: To run the Obsidian agent, run the following command from the agent root directory: 
      uv run src/a2a_mcp/agents/ --agent-card agent_cards/obsidian_agent.json --port 27121

Step 4: To run test_client, change directory to src/a2a_mcp/agents, and run python3 test_client.py