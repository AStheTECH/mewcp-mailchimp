"""
Stateless MCP Server for Mailchimp API
"""

import logging
import argparse
from fastmcp import FastMCP
from pydantic import Field
from utils.mailchimp_client import make_mailchimp_request


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
    logger.info("Mailchimp MCP Server Starting (Stateless Multi-User)")
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
