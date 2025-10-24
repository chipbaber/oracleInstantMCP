from fastmcp import FastMCP
import oracledb, os

mcp = FastMCP("My First 26ai MCP Server")

def _conn():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dsn=os.getenv("DB_DSN"),
        wallet=os.getenv("WALLET_LOCATION")
    )

