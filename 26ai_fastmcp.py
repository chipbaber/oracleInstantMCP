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

@mcp.tool()(
    name="Get-Player-Table-Column-Comments",
    description="As the players user in a 26ai Oracle Database you will query to get column comments on a inputed column", 
    tags={"teamstats", "search", "table"},      
    meta={"version": "1.0", "author": "Chip Baber"}  
)
def table_comments(table: str) -> list[dict]:
    """Get all comments for columns on a table"""
    with _conn() as con:
        cur = con.cursor()
        cur.execute("""
            select column_name, comments
            from user_col_comments
            where table_name =  :t
            ORDER BY column_id
        """, t=table.upper())
        return [{"column_name": c[0], "comments": c[1]} for c in cur]

if __name__ == "__main__":
   mcp.run(transport="http", port=8000)