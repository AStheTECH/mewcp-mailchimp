import logging
from typing import Dict, Any, Optional
from utils import make_mailchimp_request

logger = logging.getLogger("mailchimp-mcp-server")


############### Template Folder Management ###############
def list_template_folders_service(
    access_token: str,
    server: str,
    count: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }
    """
    Get all folders used to organize templates.

    Returns information for each folder including:
    - Folder ID and name
    - Number of templates in the folder
    - Date created

    """

    logger.info(f"Fetching template folders with params: {query_params}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.templateFolders.list(**query_params),
    )


def add_template_folder_service(
    access_token: str,
    server: str,
    name: str,
) -> Dict[str, Any]:
    body = {
        "name": name,
    }

    logger.info(f"Creating template folder with name: {name}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.templateFolders.create(body),
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


def add_template_service(
    access_token: str,
    server: str,
    name: str,
    html: str,
    folder_id: Optional[str] = None,
) -> Dict[str, Any]:
    body = {
        "name": name,
        "html": html,
    }

    if folder_id:
        body["folder_id"] = folder_id

    logger.info(f"Creating template with name: {name}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.templates.create(body),
    )




