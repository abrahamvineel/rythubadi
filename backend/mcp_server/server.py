from fastmcp import FastMCP

mcp = FastMCP("rythu")

from mcp_server.tools import weather, soil, crop, schemes, diagnosis # noqa: F401

if __name__ == "__main__":
    mcp.run(transport="stdio")
