from fastmcp import FastMCP
import oracledb, os

mcp = FastMCP("Baseball Player and Stat MCP Server")

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
            ORDER BY column_name
        """, t=table.upper())
        return [{"column_name": c[0], "comments": c[1]} for c in cur.fetchall()]

@mcp.tool()(
    name="Get-Players-AVG-OBP",
    description="This tool inputs a individual baseball players atbats, hits, walks, sacrifices then calculates and outputs the players batting average in three decimals (.300) and a players on base percentage in three decimals (.300). ", 
    tags={"procedure", "calculate", "baseball", "average", "On base Percentage", "hitting", "batting"},      
    meta={"version": "1.0", "author": "Chip Baber"}  
)
def getAvgOBP(atbats: int, hits: int, walks: int, sacrifices: int) -> dict:
    """Execute a procedure in the players schema to calculate and return a result"""
    try:
        with _conn() as con:
            cur = con.cursor()
            # Create the output variables
            batting_avg = cur.var(oracledb.NUMBER)
            on_base_percentage = cur.var(oracledb.NUMBER)
            # Call the stored procedure
            cur.callproc("myStats", [atbats, hits, walks, sacrifices, batting_avg, on_base_percentage])
            # Format results
            result = {
                "Batting Average": round(batting_avg.getvalue(), 3),
                "On Base Percentage": round(on_base_percentage.getvalue(), 3)
            }
            return result
    except cx_Oracle.Error as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
   mcp.run(transport="http", port=8000)