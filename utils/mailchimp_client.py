"""Shared utilities for Mailchimp API requests"""

import logging
from typing import Dict, Any

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from fastmcp_credentials import get_credentials

logger = logging.getLogger("mailchimp-mcp-server")


def get_mailchimp_client() -> MailchimpMarketing.Client:
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    server_prefix = cred.extra.get("server_prefix")
    if not server_prefix:
        raise ValueError("No server_prefix found in credential extras")
    client = MailchimpMarketing.Client()
    client.set_config({"access_token": cred.access_token, "server": server_prefix})
    return client


def make_mailchimp_request(api_method: callable) -> Dict[str, Any]:
    try:
        client = get_mailchimp_client()

        if callable(api_method):
            result = api_method(client)
        else:
            raise ValueError("api_method must be callable")

        return result

    except ApiClientError as error:
        logger.error(f"Mailchimp API error: {error.text}")
        return {
            "error": error.text if hasattr(error, "text") else str(error),
            "status": error.status_code if hasattr(error, "status_code") else None,
        }
    except Exception as e:
        logger.error(f"Request error: {e}")
        return {"error": str(e)}
