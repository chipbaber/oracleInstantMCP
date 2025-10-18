# oracle-mcp-server
Minimal MCP server implementation for Oracle AI Database 26 ai using Python.
A lightweight MCP server that exposes Oracle Database tools (`list_tables`, `describe_table`, `query`) to any MCP-compatible AI client.

# Features
- Secure, read-only SQL access via MCP protocol  
- Uses `python-oracledb` driver  
- Easily deployable on Oracle Cloud Infrastructure (OCI)  

# Setup

```bash
pip install mcp python-oracledb
export ORACLE_USER=your_username
export ORACLE_PASSWORD=your_password
export ORACLE_DSN="hostname/service_name"
python oracle_mcp.py
