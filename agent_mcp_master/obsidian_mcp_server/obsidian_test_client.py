# sse_client.py
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # SSE server URL
    server_url = "http://localhost:27122/sse"
    
    print(f"Connecting to SSE server at {server_url}...")
    
    # Create the connection via SSE transport
    async with sse_client(url=server_url) as streams:
        # Create the client session with the streams
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            response = await session.list_tools()
            print("Available tools:", [tool.name for tool in response.tools])
            
            # Call the greet tool
            result = await session.call_tool("append_content", {"file_name":  "welcome.md", "content":"pragyan adding content"})
            print("Greeting result:", result.content)
            

if __name__ == "__main__":
    asyncio.run(main())