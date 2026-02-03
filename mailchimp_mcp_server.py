"""
Stateless MCP Server for Mailchimp Marketing API
"""

import logging
import argparse
from fastmcp import FastMCP
from pydantic import Field
from typing import Optional

from tools import (
    list_automations_service,
    get_automation_info_service,
    list_automated_emails_service,
    get_workflow_email_info_service,
    list_automated_email_subscribers_service,
    get_automated_email_subscriber_service,
    list_audience_service,
    get_list_info_service,
    list_campaigns_service,
    get_campaign_info_service,
    list_templates_service,
    get_template_info_service,
)
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

######### Automation Management #########


@mcp.tool(
    name="list_automations",
    description="Get a summary of an account's classic automations with optional filtering and pagination",
)
def list_automations(
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
def get_automation_info(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
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


######### Automation Email Management #########


@mcp.tool(
    name="list_automated_emails",
    description="Get a summary of the emails in a classic automation workflow",
)
def list_automated_emails(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
):
    return list_automated_emails_service(
        access_token=oauth_token,
        server=server,
        workflow_id=workflow_id,
    )


@mcp.tool(
    name="get_workflow_email_info",
    description="Get detailed information about a specific email in an automation workflow",
)
def get_workflow_email_info(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
):
    """
    Get comprehensive information about a specific email in an automation workflow.

    Returns detailed information including:
    - Email position in the workflow sequence
    - Delay settings (when email sends relative to trigger)
    - Subject line, preview text, and content details
    - From name, reply-to, and sender settings
    - Recipients list and segment configuration
    - Tracking configuration (opens, clicks, Google Analytics)
    - Social media integration (auto-tweet, Facebook)
    - Performance metrics (open rate, click rate, sends)
    - Template and content type information
    - Current status (save, paused, sending)
    """
    return get_workflow_email_info_service(
        access_token=oauth_token,
        server=server,
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
    )


#############  Subscribers management #############


@mcp.tool(
    name="list_automated_email_subscribers",
    description="Get information about subscribers queued to receive a specific automation email",
)
def list_automated_email_subscribers(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
):
    return list_automated_email_subscribers_service(
        access_token=oauth_token,
        server=server,
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
    )


@mcp.tool(
    name="get_automated_email_subscriber",
    description="Get detailed information about a specific subscriber to an automation email queue",
)
def get_automated_email_subscriber(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
    subscriber_hash: str = Field(
        description="The MD5 hash of the lowercase version of the subscriber's email address"
    ),
):
    """
    Get information about a specific subscriber in a classic automation email queue.

    Returns detailed information about a queued subscriber:
    - Email address and subscriber ID
    - List membership information
    - Next scheduled send time
    - Queue position and priority
    - Workflow and email IDs
    - Links to related resources

    This is useful for:
    - Checking if a specific subscriber is queued for an email
    - Verifying when an email will be sent to a subscriber
    - Troubleshooting automation delivery for individual contacts
    - Monitoring subscriber progress through automation workflows

    Note: subscriber_hash is the MD5 hash of the lowercase email address.
    Example: email@example.com -> 5d41402abc4b2a76b9719d911017c592
    """
    return get_automated_email_subscriber_service(
        access_token=oauth_token,
        server=server,
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
        subscriber_hash=subscriber_hash,
    )


############### List Management ###############


@mcp.tool(
    name="list_audience",
    description="Get information about all lists (audiences) in the account",
)
def list_audience(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
):
    """
    Get information about all lists (audiences) in the account.

    Returns detailed information for each list including:
    - List ID, name, and web ID
    - Contact information (company, address, phone)
    - Permission reminder and campaign defaults
    - Statistics (member count, unsubscribe count, cleaned count, etc.)
    - Date created and date of last campaign sent
    - List rating and visibility settings
    """
    return list_audience_service(
        access_token=oauth_token,
        server=server,
    )


@mcp.tool(
    name="get_list_info",
    description="Get detailed information about a specific list (audience) in your Mailchimp account",
)
def get_list_info(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    list_id: str = Field(description="The unique ID for the list"),
):
    return get_list_info_service(
        access_token=oauth_token,
        server=server,
        list_id=list_id,
    )


############### Campaign Management ###############


@mcp.tool(name="list_campaigns", description="Get all campaigns in an account")
def list_campaigns(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
):
    return list_campaigns_service(
        access_token=oauth_token,
        server=server,
    )


@mcp.tool(
    name="get_campaign_info",
    description="Get detailed information about a specific campaign",
)
def get_campaign_info(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    campaign_id: str = Field(description="The unique ID for the campaign"),
):
    return get_campaign_info_service(
        access_token=oauth_token,
        server=server,
        campaign_id=campaign_id,
    )


############### Template Management ###############
@mcp.tool(name="list_templates", description="Get all templates in your account")
def list_templates(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    count: int = Field(
        default=10, description="Number of templates to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
    type: Optional[str] = Field(
        default=None, description="Filter by type: 'user', 'base', or 'gallery'"
    ),
    content_type: Optional[str] = Field(
        default=None,
        description="Filter by content type: 'html', 'template', or 'multichannel'",
    ),
):
    return list_templates_service(
        access_token=oauth_token,
        server=server,
        count=count,
        offset=offset,
        type=type,
        content_type=content_type,
    )


@mcp.tool(
    name="get_template_info",
    description="Get detailed information about a specific template by ID",
)
def get_template_info(
    oauth_token: str = Field(description="OAuth access token"),
    server: str = Field(description="Server prefix (e.g., 'us18')"),
    template_id: str = Field(description="The unique ID for the template"),
):
    return get_template_info_service(
        access_token=oauth_token,
        server=server,
        template_id=template_id,
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
