from fastmcp import FastMCP
import oracledb, os

mcp = FastMCP("My First 26ai MCP Server")


# Function to create a database connection
def _conn():
    try:
        #Set instant client directory on the machine running the code
        instant_client_dir = os.getenv("INSTANT_CLIENT_DIR", "")
        oracledb.init_oracle_client(lib_dir=instant_client_dir)
        #attempt to make the connection
        conn = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            dsn=os.getenv("DB_DSN"),
            config_dir=os.getenv("WALLET_LOCATION")
        )
        return conn
    except oracledb.Error as error:
        st.error(f"Error connecting to Oracle Database: {error}")
        return None

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
            ORDER BY column_name asc
        """, t=table.upper())
        return [{"column_name": c[0], "comments": c[1]} for c in cur]

if __name__ == "__main__":
   mcp.run(transport="http", port=8000)