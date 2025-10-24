import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

"""
async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)
"""
"""First example DB MCP Call """
async def call_tool(name: str):
    async with client:
        result = await client.call_tool("Get-Player-Table-Column-Comments", {"table": name})
        print(result)


asyncio.run(call_tool("TEAMSTATS"))