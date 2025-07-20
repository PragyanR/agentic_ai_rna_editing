from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn
import os
import logging
 
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("ObsidianMCPServer")

# import API for accessing Obsedian
import obsidian

# update your env or change the values here
api_key = os.getenv("OBSIDIAN_API_KEY", "6ff926d87935a331be329f1fe8d4219a9f706474d8c19bec31cd7a2405b904d2")

obsidian_mcp_server_host = "localhost"
obsidian_mcp_server_port = 27122

@mcp.tool(
    name="add_obsidian_content",           
    description="Add or update content to Obsidian"  )
async def add_obsidian_content(file_name, content) -> str:
    status = "Pending update"
    logger.info(f"Updating file: {file_name}")
    try:
        if file_name is None or content is None:
            logger.info("Missing Params file_name and content")
            raise RuntimeError("obsidian_file and content arguments required")
        
        api = obsidian.Obsidian(api_key, host=obsidian_mcp_server_host)
        api.append_content(file_name, content)
        status = f'Successfully updated {file_name}'
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        status = f'Failed to update {file_name}'

    return status


@mcp.tool(
    name="list_obsidian_files",           
    description="list files in Obsidian" )
async def list_obsidian_files() -> str:
    try:
        api = obsidian.Obsidian(api_key, host=obsidian_mcp_server_host)
        files = api.list_files_in_vault()
        logger.info(f'Files in vault:{files}')
        return files
    except Exception as e:
        logger.info(f"failed to list files becuase: {e}")
        return f"failed to list files becuase: {e}"


@mcp.tool(
    name="create_obsidian_file",           
    description="Create a file in Obsidian" )
async def create_obsidian_file(file_name) -> str:
    status = "Pending creation"
    try:
        if file_name is None:
            logger.info("Missing Params file_name")
            raise RuntimeError("obsidian_file argument required")
        api = obsidian.Obsidian(api_key, host=obsidian_mcp_server_host)
        api.append_content(file_name,"")
        status = f"created file: {file_name}"
    except Exception as e:
        status = f"failed to list files becuase: {e}"
    
    return status

@mcp.tool(
    name="get_obsidian_content",           
    description="Get Obsidian Content" )
async def get_obsidian_content(file_name) -> str:
    logger.info(f"Getting content from file: {file_name}")
    try:
        if file_name is None:
            logger.info("Missing Params file_name")
            raise RuntimeError("obsidian_file argument required")
        
        api = obsidian.Obsidian(api_key, host=obsidian_mcp_server_host)
        files = api.list_files_in_vault()
        if file_name in files:
            return api.get_file_contents(file_name)
        else:
            return f"{file_name} not found" 

    except Exception as e:
        return f"failed to get content from {file_name} becuase: {e}"

@mcp.tool(
    name="delete_obsidian_file",           
    description="Delete Obsidian file" )
async def delete_obsidian_file(file_name) -> str:
    logger.info(f'Deleting file: {file_name}')
    try:
        if file_name is None:
            logger.info("Missing Params file_name")
            raise RuntimeError("obsidian_file argument required")
        
        api = obsidian.Obsidian(api_key, host=obsidian_mcp_server_host)
        files = api.list_files_in_vault()
        if file_name in files:
            return api.delete_file(file_name)
        else:
            return f"{file_name} not found"

    except Exception as e:
        return f"failed to get content from {file_name} becuase: {e}"
    
    

     
       

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the MCP server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

if __name__ == "__main__":
    # Get the underlying MCP server
    mcp_server = mcp._mcp_server
    
    # Create Starlette app with SSE support
    starlette_app = create_starlette_app(mcp_server, debug=True)
    
    port = 27122
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    
    # Run the server using uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)