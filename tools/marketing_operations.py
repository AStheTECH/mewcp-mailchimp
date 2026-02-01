"""Service layer for Mailchimp Automation operations"""

import logging
from typing import Dict, Any, Optional
from utils import make_mailchimp_request

logger = logging.getLogger("mailchimp-mcp-server")


############## Automation Management ##############
def list_automations_service(
    access_token: str,
    server: str,
    count: int = 10,
    offset: int = 0,
    fields: Optional[list] = None,
    exclude_fields: Optional[list] = None,
    before_create_time: Optional[str] = None,
    since_create_time: Optional[str] = None,
    before_start_time: Optional[str] = None,
    since_start_time: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    # Build query parameters
    query_params = {
        "count": count,
        "offset": offset,
    }

    # Add optional parameters
    if fields:
        query_params["fields"] = ",".join(fields)
    if exclude_fields:
        query_params["exclude_fields"] = ",".join(exclude_fields)
    if before_create_time:
        query_params["before_create_time"] = before_create_time
    if since_create_time:
        query_params["since_create_time"] = since_create_time
    if before_start_time:
        query_params["before_start_time"] = before_start_time
    if since_start_time:
        query_params["since_start_time"] = since_start_time
    if status:
        # Validate status
        valid_statuses = ["save", "paused", "sending"]
        if status not in valid_statuses:
            return {
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                "status": 400,
            }
        query_params["status"] = status

    logger.info(f"Fetching automations with params: {query_params}")

    # Make API request
    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.list(**query_params),
    )


def get_automation_info_service(
    access_token: str,
    server: str,
    workflow_id: str,
    fields: Optional[list] = None,
    exclude_fields: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Get a summary of an individual classic automation workflow's settings and content.

    Args:
        access_token: OAuth access token
        server: Server prefix (e.g., 'us18')
        workflow_id: The unique id for the Automation workflow
        fields: List of fields to return
        exclude_fields: List of fields to exclude

    Returns:
        Dict containing automation details or error
    """
    # Build query parameters
    query_params = {}

    if fields:
        query_params["fields"] = ",".join(fields)
    if exclude_fields:
        query_params["exclude_fields"] = ",".join(exclude_fields)

    logger.info(f"Fetching automation info for workflow_id: {workflow_id}")

    # Make API request
    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.get(workflow_id, **query_params),
    )


################# Automation Email Management #################


def list_automated_emails_service(
    access_token: str,
    server: str,
    workflow_id: str,
) -> Dict[str, Any]:
    logger.info(f"Fetching automated emails for workflow_id: {workflow_id}")
    """


    Returns detailed information for each email including:
    - Email position in workflow and delay settings
    - Subject line, preview text, and content details
    - Recipients and segment information
    - Tracking configuration (opens, clicks, analytics)
    - Social media settings
    - Report summary (performance metrics)
    - Send time and status
    """

    # Make API request
    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.list_all_workflow_emails(
            workflow_id
        ),
    )
