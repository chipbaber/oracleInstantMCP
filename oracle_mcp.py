# oracle_mcp.py
from mcp.server.fastmcp import FastMCP
import oracledb, os

mcp = FastMCP("oracle-mcp")

def _conn():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )

@mcp.tool()
def list_tables(owner: str) -> list[dict]:
    """List tables for an OWNER (schema)."""
    with _conn() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT table_name
            FROM all_tables
            WHERE owner = :o
            ORDER BY table_name
        """, o=owner.upper())
        return [{"table_name": r[0]} for r in cur.fetchall()]

@mcp.tool()
def describe_table(owner: str, table: str) -> list[dict]:
    """Describe columns for OWNER.TABLE."""
    with _conn() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT column_name, data_type, data_length, nullable
            FROM all_tab_columns
            WHERE owner = :o AND table_name = :t
            ORDER BY column_id
        """, o=owner.upper(), t=table.upper())
        return [{"column_name": c[0], "data_type": c[1], "len": c[2], "nullable": c[3]} for c in cur]

@mcp.tool()
def query(sql: str) -> list[dict]:
    """Execute a read-only SELECT."""
    s = sql.strip().lower()
    assert s.startswith("select"), "Only SELECT allowed"
    with _conn() as con:
        cur = con.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

if __name__ == "__main__":
    mcp.run_stdio()
