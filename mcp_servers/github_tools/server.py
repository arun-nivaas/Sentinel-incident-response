import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from github_client import GitHubClient
from typing import Any

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("github-incident-tools")


@mcp.tool()
def create_github_issue(title: str, body: str, severity: str = "unknown") -> Any:
    """Create a GitHub issue documenting a production incident.

    Args:
        title: Short issue title, e.g. service name + error type
        body: Full markdown-formatted issue body
        severity: Severity level (P1-P4) to add as a label
    """
    
    logger.info(f"Received create_github_issue call: {title}")
    client = GitHubClient()
    labels = [severity] if severity != "unknown" else []
    result = client.create_issue(title=title, body=body, labels=labels)
    logger.info(f"Issue created: {result['issue_url']}")

    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")