"""Shared utilities for Mailchimp API requests"""

import logging
from typing import Dict, Any

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger("mailchimp-mcp-server")


def get_mailchimp_client(access_token: str, server: str) -> MailchimpMarketing.Client:
    """Initialize Mailchimp client with OAuth access token - stateless per request"""
    client = MailchimpMarketing.Client()
    client.set_config({"access_token": access_token, "server": server})
    return client


def make_mailchimp_request(
    access_token: str, server: str, api_method: callable, *args, **kwargs
) -> Dict[str, Any]:
    try:
        client = get_mailchimp_client(access_token, server)

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


# \
