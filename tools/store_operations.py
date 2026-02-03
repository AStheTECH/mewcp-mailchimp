import logging
from typing import Dict, Any, Optional
from utils import make_mailchimp_request

logger = logging.getLogger("mailchimp-mcp-server")

############ E-commerce Store Operations ############


def list_stores_service(
    access_token: str,
    server: str,
    count: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }

    logger.info(f"Fetching e-commerce stores with params: {query_params}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.ecommerce.stores(**query_params),
    )


def get_store_info_service(
    access_token: str,
    server: str,
    store_id: str,
) -> Dict[str, Any]:
    logger.info(f"Fetching store info for store_id: {store_id}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.ecommerce.get_store(store_id),
    )


def list_products_service(
    access_token: str,
    server: str,
    store_id: str,
    count: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }

    logger.info(
        f"Fetching products for store_id: {store_id} with params: {query_params}"
    )

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.ecommerce.get_all_store_products(
            store_id, **query_params
        ),
    )


def get_product_info_service(
    access_token: str,
    server: str,
    store_id: str,
    product_id: str,
) -> Dict[str, Any]:
    logger.info(
        f"Fetching product info for store_id: {store_id}, product_id: {product_id}"
    )

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.ecommerce.get_store_product(
            store_id, product_id
        ),
    )


def list_store_orders_service(
    access_token: str,
    server: str,
    store_id: str,
    count: int = 10,
    offset: int = 0,
    customer_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
) -> Dict[str, Any]:
    query_params = {
        "count": count,
        "offset": offset,
    }

    if customer_id:
        query_params["customer_id"] = customer_id
    if campaign_id:
        query_params["campaign_id"] = campaign_id

    logger.info(f"Fetching orders for store_id: {store_id} with params: {query_params}")

    return make_mailchimp_request(
        access_token=access_token,
        server=server,
        api_method=lambda client: client.ecommerce.get_store_orders(
            store_id, **query_params
        ),
    )
