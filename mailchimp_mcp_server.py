"""
Stateless MCP Server for Mailchimp Marketing API
"""

import logging
import argparse
from fastmcp import FastMCP
from pydantic import Field
from typing import Optional
from tools import list_automations_service, get_automation_info_service
from utils import make_mailchimp_request


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("mailchimp-mcp-server")

# FastMCP instance
mcp = FastMCP("Mailchimp MCP Server")


# ============== Health Check ==============


@mcp.tool(name="health_check", description="Check Mailchimp API connectivity")
def health_check(oauth_token: str, server: str):
    return make_mailchimp_request(
        access_token=oauth_token,
        server=server,
        api_method=lambda client: client.ping.get(),
    )


# ============== Tools ==============


@mcp.tool(
    name="list_automations",
    description="Get a summary of an account's classic automations with optional filtering and pagination",
)
def list_automations_tool(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    count: int = Field(
        default=10, description="Number of records to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
    fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to return"
    ),
    exclude_fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to exclude"
    ),
    before_create_time: Optional[str] = Field(
        default=None,
        description="Restrict to automations created before this time (ISO 8601: 2015-10-21T15:41:36+00:00)",
    ),
    since_create_time: Optional[str] = Field(
        default=None,
        description="Restrict to automations created after this time (ISO 8601: 2015-10-21T15:41:36+00:00)",
    ),
    before_start_time: Optional[str] = Field(
        default=None,
        description="Restrict to automations started before this time (ISO 8601: 2015-10-21T15:41:36+00:00)",
    ),
    since_start_time: Optional[str] = Field(
        default=None,
        description="Restrict to automations started after this time (ISO 8601: 2015-10-21T15:41:36+00:00)",
    ),
    status: Optional[str] = Field(
        default=None, description="Filter by status: 'save', 'paused', or 'sending'"
    ),
):
    fields_list = fields.split(",") if fields else None
    exclude_fields_list = exclude_fields.split(",") if exclude_fields else None

    return list_automations_service(
        access_token=oauth_token,
        server=server,
        count=count,
        offset=offset,
        fields=fields_list,
        exclude_fields=exclude_fields_list,
        before_create_time=before_create_time,
        since_create_time=since_create_time,
        before_start_time=before_start_time,
        since_start_time=since_start_time,
        status=status,
    )


@mcp.tool(
    name="get_automation_info",
    description="Get detailed information about a specific automation workflow by ID",
)
def get_automation_info_tool(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID for the Automation workflow"),
    fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to return"
    ),
    exclude_fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to exclude"
    ),
):
    """
    Get a summary of an individual classic automation workflow's settings and content.

    Returns detailed information including:
    - Workflow settings (title, from name, reply to, etc.)
    - Recipients and list information
    - Trigger settings and workflow type
    - Tracking configuration
    - Report summary (opens, clicks, rates)
    """
    fields_list = fields.split(",") if fields else None
    exclude_fields_list = exclude_fields.split(",") if exclude_fields else None

    return get_automation_info_service(
        access_token=oauth_token,
        server=server,
        workflow_id=workflow_id,
        fields=fields_list,
        exclude_fields=exclude_fields_list,
    )


########## Parsing Args ##########


def parse_args():
    parser = argparse.ArgumentParser(description="Mailchimp MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method: 'stdio', 'sse', or 'streamable-http'",
        default="streamable-http",
    )
    parser.add_argument("--host", help="Host to bind to", default="0.0.0.0")
    parser.add_argument("--port", type=int, help="Port to bind to", default=8000)
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Mailchimp marketing MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
    if args.host:
        run_kwargs["host"] = args.host
    if args.port:
        run_kwargs["port"] = args.port

    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
