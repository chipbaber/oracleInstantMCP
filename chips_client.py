import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

"""First example DB MCP Call 
async def call_tool(tablename: str):
    async with client:
        result = await client.call_tool("Get-Table-Column-Comments", {"table": tablename})
        print(result)


asyncio.run(call_tool("TEAMSTATS"))
"""

"""MCP Call a DB Procedure 
async def call_tool(ab: int, h: int, w: int, sac: int):
    async with client:
        result = await client.call_tool("Get-Players-AVG-OBP", {"atbats": ab, "hits": h, "walks": w, "sacrifices": sac})
        print(result)


asyncio.run(call_tool(10,2,1,1))
"""

"""MCP Call a DB Query"""
async def call_tool(p: str):
    async with client:
        result = await client.call_tool("Get-Players-Stats", {"player_name": p})
        print(result)


asyncio.run(call_tool("Tank"))