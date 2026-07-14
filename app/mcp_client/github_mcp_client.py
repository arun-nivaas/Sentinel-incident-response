import sys
import json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any,Dict
from langsmith import traceable #type: ignore
from app.core.logger import logger

SERVER_SCRIPT = str(
    Path(__file__).resolve().parents[2] / "mcp_servers" / "github_tools" / "server.py"
)


class GitHubMCPClient:
    @traceable(name="github_action", tags=["github-action"])
    async def create_github_issue(self, title: str, body: str, severity: str = "unknown") -> Dict[str, Any]:
        server_params = StdioServerParameters(
            command=sys.executable,   
            args=[SERVER_SCRIPT],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                logger.info("Connected to GitHub MCP server, listing tools...")
                tools = await session.list_tools()
                logger.debug(f"Available tools: {[t.name for t in tools.tools]}")

                result = await session.call_tool(
                    "create_github_issue",
                    arguments={"title": title, "body": body, "severity": severity},
                )

                if result.content and hasattr(result.content[0], "text"):
                    return json.loads(result.content[0].text) #type: ignore

                raise RuntimeError("Unexpected MCP tool result format")