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
    list_campaign_reports_service,
    get_campaign_report_service,
    list_landing_pages_service,
    get_landing_page_info_service,
    get_landing_page_content_service,
    list_template_folders_service,
    add_template_folder_service,
    add_template_service,
    update_template_service,
    list_stores_service,
    get_store_info_service,
    list_products_service,
    get_product_info_service,
    list_store_orders_service,
    get_order_info_service,
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
mcp = FastMCP("MewCP Mailchimp MCP Server")

# Expose ASGI app for hosting platform's (e.g. Vercel) Python runtime.
app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)


# ============== Health Check ==============


@mcp.tool(name="health_check", description="Check Mailchimp API connectivity")
def health_check():
    return make_mailchimp_request(
        api_method=lambda client: client.ping.get(),
    )


# ============== Tools ==============

######### Automation Management #########


@mcp.tool(
    name="list_automations",
    description="Get a summary of an account's classic automations with optional filtering and pagination",
)
def list_automations(
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
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to return"
    ),
    exclude_fields: Optional[str] = Field(
        default=None, description="Comma-separated list of fields to exclude"
    ),
):

    fields_list = fields.split(",") if fields else None
    exclude_fields_list = exclude_fields.split(",") if exclude_fields else None

    return get_automation_info_service(
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
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
):
    return list_automated_emails_service(
        workflow_id=workflow_id,
    )


@mcp.tool(
    name="get_workflow_email_info",
    description="Get detailed information about a specific email in an automation workflow",
)
def get_workflow_email_info(
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
):
    """

    Returns:
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
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
    )


#############  Subscribers management #############


@mcp.tool(
    name="list_automated_email_subscribers",
    description="Get information about subscribers queued to receive a specific automation email",
)
def list_automated_email_subscribers(
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
):
    return list_automated_email_subscribers_service(
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
    )


@mcp.tool(
    name="get_automated_email_subscriber",
    description="Get detailed information about a specific subscriber to an automation email queue",
)
def get_automated_email_subscriber(
    workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    workflow_email_id: str = Field(
        description="The unique ID of the Automation workflow email"
    ),
    subscriber_hash: str = Field(
        description="The MD5 hash of the lowercase version of the subscriber's email address"
    ),
):

    return get_automated_email_subscriber_service(
        workflow_id=workflow_id,
        workflow_email_id=workflow_email_id,
        subscriber_hash=subscriber_hash,
    )


############### List Management ###############


@mcp.tool(
    name="list_audience",
    description="Get information about all lists (audiences) in the account",
)
def list_audience():

    return list_audience_service()


@mcp.tool(
    name="get_list_info",
    description="Get detailed information about a specific list (audience) in your Mailchimp account",
)
def get_list_info(
    list_id: str = Field(description="The unique ID for the list"),
):
    return get_list_info_service(
        list_id=list_id,
    )


############### Campaign Management ###############


@mcp.tool(name="list_campaigns", description="Get all campaigns in an account")
def list_campaigns():
    return list_campaigns_service()


@mcp.tool(
    name="get_campaign_info",
    description="Get detailed information about a specific campaign",
)
def get_campaign_info(
    campaign_id: str = Field(description="The unique ID for the campaign"),
):
    return get_campaign_info_service(
        campaign_id=campaign_id,
    )


############### Folder Management ###############


@mcp.tool(
    name="list_template_folders",
    description="Get all folders used to organize templates",
)
def list_template_folders(
    count: int = Field(
        default=10, description="Number of folders to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
):
    return list_template_folders_service(
        count=count,
        offset=offset,
    )


# Add after list_template_folders tool


@mcp.tool(name="add_template_folder", description="Create a new template folder")
def add_template_folder(
    name: str = Field(description="The name of the folder"),
):
    return add_template_folder_service(
        name=name,
    )


############### Template Management ###############
@mcp.tool(name="list_templates", description="Get all templates in your account")
def list_templates(
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
    template_id: str = Field(description="The unique ID for the template"),
):
    return get_template_info_service(
        template_id=template_id,
    )


@mcp.tool(
    name="add_template",
    description="Create a new Classic template for the account. it support Mailchimp Template Language",
)
def add_template(
    name: str = Field(description="The name of the template"),
    html: str = Field(
        description="The raw HTML for the template. Supports Mailchimp Template Language"
    ),
    folder_id: Optional[str] = Field(
        default=None, description="The ID of the folder to place the template in"
    ),
):
    return add_template_service(
        name=name,
        html=html,
        folder_id=folder_id,
    )


@mcp.tool(
    name="update_template",
    description="Update the name, HTML, or folder of an existing template",
)
def update_template(
    template_id: str = Field(description="The unique ID for the template"),
    name: str = Field(description="The name of the template"),
    html: str = Field(
        description="The raw HTML for the template. Supports Mailchimp Template Language"
    ),
    folder_id: Optional[str] = Field(
        default=None, description="The ID of the folder to move the template to"
    ),
):
    return update_template_service(
        template_id=template_id,
        name=name,
        html=html,
        folder_id=folder_id,
    )


############### Campaign Report Management ###############


@mcp.tool(
    name="list_campaign_reports",
    description="Get all  campaign reports with performance metrics",
)
def list_campaign_reports(
    count: int = Field(
        default=10, description="Number of reports to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
    type: Optional[str] = Field(
        default=None,
        description="Filter by campaign type: 'regular', 'plaintext', 'absplit', 'rss', or 'variate'",
    ),
):
    return list_campaign_reports_service(
        count=count,
        offset=offset,
        type=type,
    )


@mcp.tool(
    name="get_campaign_report",
    description="Get detailed report for a specific sent campaign",
)
def get_campaign_report(
    campaign_id: str = Field(description="The unique ID for the campaign"),
):
    return get_campaign_report_service(
        campaign_id=campaign_id,
    )


############### Landing Pages ###############


@mcp.tool(
    name="list_landing_pages", description="Get all landing pages in your account"
)
def list_landing_pages(
    count: int = Field(
        default=10, description="Number of landing pages to return (max: 1000)"
    ),
    sort_field: Optional[str] = Field(
        default=None, description="Sort by: 'created_at' or 'updated_at'"
    ),
    sort_dir: Optional[str] = Field(
        default=None, description="Sort direction: 'ASC' or 'DESC'"
    ),
):
    return list_landing_pages_service(
        count=count,
        sort_field=sort_field,
        sort_dir=sort_dir,
    )


@mcp.tool(
    name="get_landing_page_info",
    description="Get detailed information about a specific landing page by ID",
)
def get_landing_page_info(
    page_id: str = Field(description="The unique ID for the landing page"),
):
    return get_landing_page_info_service(
        page_id=page_id,
    )


@mcp.tool(
    name="get_landing_page_content",
    description="Get the HTML content for a specific landing page",
)
def get_landing_page_content(
    page_id: str = Field(description="The unique ID for the landing page"),
):
    return get_landing_page_content_service(
        page_id=page_id,
    )


@mcp.tool(
    name="list_stores",
    description="Get information about all e-commerce stores in the account",
)
def list_stores(
    count: int = Field(
        default=10, description="Number of stores to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
):
    return list_stores_service(
        count=count,
        offset=offset,
    )


@mcp.tool(
    name="get_store_info",
    description="Get detailed information about a specific e-commerce store",
)
def get_store_info(
    store_id: str = Field(description="The unique ID for the store"),
):
    return get_store_info_service(
        store_id=store_id,
    )


@mcp.tool(
    name="list_products",
    description="Get information about all products in a specific e-commerce store",
)
def list_products(
    store_id: str = Field(description="The unique ID for the store"),
    count: int = Field(
        default=10, description="Number of products to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
):
    return list_products_service(
        store_id=store_id,
        count=count,
        offset=offset,
    )


@mcp.tool(
    name="get_product_info",
    description="Get detailed information about a specific product in an e-commerce store",
)
def get_product_info(
    store_id: str = Field(description="The unique ID for the store"),
    product_id: str = Field(description="The unique ID for the product"),
):
    return get_product_info_service(
        store_id=store_id,
        product_id=product_id,
    )


@mcp.tool(
    name="list_store_orders",
    description="Get information about all orders in a specific e-commerce store",
)
def list_store_orders(
    store_id: str = Field(description="The unique ID for the store"),
    count: int = Field(
        default=10, description="Number of orders to return (max: 1000)"
    ),
    offset: int = Field(
        default=0, description="Number of records to skip for pagination"
    ),
    customer_id: Optional[str] = Field(
        default=None,
        description="Restrict results to orders made by a specific customer",
    ),
    campaign_id: Optional[str] = Field(
        default=None,
        description="Restrict results to orders with a specific campaign ID",
    ),
):
    return list_store_orders_service(
        store_id=store_id,
        count=count,
        offset=offset,
        customer_id=customer_id,
        campaign_id=campaign_id,
    )


@mcp.tool(
    name="get_order_info",
    description="Get detailed information about a specific order in an e-commerce store",
)
def get_order_info(
    store_id: str = Field(description="The unique ID for the store"),
    order_id: str = Field(description="The unique ID for the order"),
):
    return get_order_info_service(
        store_id=store_id,
        order_id=order_id,
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
