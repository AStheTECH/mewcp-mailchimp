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
    query_params = {
        "count": count,
        "offset": offset,
    }

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

    query_params = {}

    if fields:
        query_params["fields"] = ",".join(fields)
    if exclude_fields:
        query_params["exclude_fields"] = ",".join(exclude_fields)

    logger.info(f"Fetching automation info for workflow_id: {workflow_id}")

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

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.list_all_workflow_emails(
            workflow_id
        ),
    )


def get_workflow_email_info_service(
    access_token: str,
    server: str,
    workflow_id: str,
    workflow_email_id: str,
) -> Dict[str, Any]:
    """
    Returns:
        Dict containing detailed email information including:
        - Email settings (subject, preview text, from name)
        - Delay and trigger configuration
        - Recipients and segment information
        - Tracking settings (opens, clicks, analytics)
        - Social media integration
        - Report summary with performance metrics
        - Content type and template information
    """
    logger.info(
        f"Fetching workflow email info - workflow_id: {workflow_id}, email_id: {workflow_email_id}"
    )

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.get_workflow_email(
            workflow_id, workflow_email_id
        ),
    )


def list_automated_email_subscribers_service(
    access_token: str,
    server: str,
    workflow_id: str,
    workflow_email_id: str,
) -> Dict[str, Any]:
    """

    Returns information about subscribers currently queued to receive this email:
    - List of subscribers in the queue
    - Email addresses and contact details
    - List membership information
    - Scheduled send times for each subscriber
    - Total count of queued subscribers
    - Queue position and priority

    This is useful for:
    - Monitoring upcoming automation sends
    - Verifying subscribers are in the correct queue
    - Checking when emails will be sent to specific contacts
    - Troubleshooting automation delivery issues
    """
    logger.info(
        f"Fetching email queue - workflow_id: {workflow_id}, email_id: {workflow_email_id}"
    )

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.get_workflow_email_subscriber_queue(
            workflow_id, workflow_email_id
        ),
    )


def get_automated_email_subscriber_service(
    access_token: str,
    server: str,
    workflow_id: str,
    workflow_email_id: str,
    subscriber_hash: str,
) -> Dict[str, Any]:
    """
    Get information about a specific subscriber in a classic automation email queue.

    Args:
        access_token: OAuth access token
        server: Server prefix (e.g., 'us18')
        workflow_id: The unique id for the Automation workflow
        workflow_email_id: The unique id for the Automation workflow email
        subscriber_hash: The MD5 hash of the lowercase version of the list member's email address

    Returns:
        Dict containing subscriber queue information including:
        - Subscriber email and ID
        - List membership details
        - Scheduled send time
        - Queue position
        - Workflow and email IDs
    """
    logger.info(
        f"Fetching subscriber from email queue - workflow: {workflow_id}, "
        f"email: {workflow_email_id}, subscriber: {subscriber_hash}"
    )

    # Make API request
    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.automations.get_workflow_email_subscriber(
            workflow_id, workflow_email_id, subscriber_hash
        ),
    )


############### List Management ###############
def list_audience_service(
    access_token: str,
    server: str,
) -> Dict[str, Any]:
    """
    Get information about all lists (audiences) in the account.
    """
    logger.info("Fetching all audiences")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.lists.get_all_lists(),
    )


def get_list_info_service(
    access_token: str,
    server: str,
    list_id: str,
) -> Dict[str, Any]:
    """
    Get information about a specific list in your Mailchimp account.

    Results include list members who have signed up but haven't confirmed
    their subscription yet and unsubscribed or cleaned.

    Returns:
        Dict containing detailed list information
    """
    logger.info(f"Fetching list info for list_id: {list_id}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.lists.get_list(list_id),
    )


############### Campaign Management ###############


def list_campaigns_service(
    access_token: str,
    server: str,
) -> Dict[str, Any]:
    """
    Get all campaigns in an account.
    """
    logger.info("Fetching all campaigns")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.campaigns.list(),
    )


def get_campaign_info_service(
    access_token: str,
    server: str,
    campaign_id: str,
) -> Dict[str, Any]:
    """
    Get information about a specific campaign.
    """
    logger.info(f"Fetching campaign info for campaign_id: {campaign_id}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.campaigns.get(campaign_id),
    )


############### Template Management ###############


def list_templates_service(
    access_token: str,
    server: str,
    count: int = 10,
    offset: int = 0,
    type: Optional[str] = None,
    content_type: Optional[str] = None,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }

    if type:
        query_params["type"] = type
    if content_type:
        if content_type not in ["html", "template", "multichannel"]:
            return {
                "error": "Invalid content_type. Must be: html, template, or multichannel",
                "status": 400,
            }
        query_params["content_type"] = content_type

    logger.info(f"Fetching templates with params: {query_params}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.templates.list(**query_params),
    )


def get_template_info_service(
    access_token: str,
    server: str,
    template_id: str,
) -> Dict[str, Any]:
    logger.info(f"Fetching template info for template_id: {template_id}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.templates.get_template(template_id),
    )


############### Campaign Report Management ###############


def list_campaign_reports_service(
    access_token: str,
    server: str,
    count: int = 10,
    offset: int = 0,
    type: Optional[str] = None,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }

    if type:
        valid_types = ["regular", "plaintext", "absplit", "rss", "variate"]
        if type not in valid_types:
            return {
                "error": f"Invalid type. Must be one of: {', '.join(valid_types)}",
                "status": 400,
            }
        query_params["type"] = type

    logger.info(f"Fetching campaign reports with params: {query_params}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.reports.get_all_campaign_reports(
            **query_params
        ),
    )


def get_campaign_report_service(
    access_token: str,
    server: str,
    campaign_id: str,
) -> Dict[str, Any]:
    logger.info(f"Fetching campaign report for campaign_id: {campaign_id}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.reports.get_campaign_report(campaign_id),
    )
