from fastmcp import FastMCP
from typing import Annotated
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


# MCP Tool to retrive stats for a player
@mcp.tool()(
    name="Get-Players-Stats",
    description="Query the Teamstats table to return the stats for a player based on an inputed name.", 
    tags={"comments", "search", "table", "baseball statistics"},      
    meta={"version": "1.0", "author": "Chip Baber"}  
)
def player_stats(player_name: str) -> list[dict]:
    """Get stats for a player name or number"""
    with _conn() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT jersey, name, gp, pa, ab, h, bb, sac, hbp, c1b, c2b, c3b, hr, rbi, r, sb 
            FROM teamstats 
            WHERE UPPER(name) LIKE :name
        """, {'name': f'{player_name.upper()}%'})
        return [{"Jersey Number": c[0], "Name": c[1],"Games Played": c[2],"Plate Appearances": c[3],"At Bats": c[4],
        "Hits": c[5],"Walks": c[6],"Sacrifices": c[7],"Hit by Pitches": c[8],"Singles": c[9],"Doubles": c[10],"Triples": c[11],"Homeruns": c[12],
        "Runs Batted In": c[13],"Runs": c[14],"Stolen Bases": c[15],} for c in cur.fetchall()]


# MCP Tool to show how to call a 26ai Autonomous database procedure to perform a calculation.
@mcp.tool()(
    name="Get-Players-AVG-OBP",
    description="This tool inputs a individual baseball players atbats, hits, walks, sacrifices then calculates and outputs the players batting average in three decimals (.300) and a players on base percentage in three decimals (.300). ", 
    tags={"procedure", "calculate", "baseball", "average", "On base Percentage", "hitting", "batting"},      
    meta={"version": "1.0", "author": "Chip Baber"},
    annotations={
        "title": "Calculate a batting average and on base percentage.",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
def getAvgOBP(atbats: Annotated[int,"Input variable for the number of at bats a baseball player has in a game or season."],
    hits: Annotated[int,"Input variable for the number of hits a baseball player has in a game or season."],
    walks_hbp: Annotated[int, "Input variable for the total number of walks added to the total number of hit by pitches a baseball player has in a game or season."],
    sacrifices: Annotated[int,"Input variable for the number of at sacrifices a baseball player has in a game or season."]
    ) -> dict:
    """Execute a procedure in the players schema to calculate and return a result"""
    try:
        with _conn() as con:
            cur = con.cursor()
            # Create the output variables
            batting_avg = cur.var(oracledb.NUMBER)
            on_base_percentage = cur.var(oracledb.NUMBER)
            # Call the stored procedure
            cur.callproc("myStats", [atbats, hits, walks_hbp, sacrifices, batting_avg, on_base_percentage])
            # Format results
            result = {
                "Batting Average": format(batting_avg.getvalue(), '.3f'),
                "On Base Percentage": format(on_base_percentage.getvalue(), '.3f'),
            }
            return result
    except oracledb.Error as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        return None

# MCP Tool to get the metadata for the columns on a table
@mcp.tool()(
    name="Get-Table-Column-Comments",
    description="As the players user in a 26ai Oracle Database you will query to get column comments for the inputted table.", 
    tags={"comments", "search", "table"},      
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

if __name__ == "__main__":
   mcp.run(transport="http", port=8000)