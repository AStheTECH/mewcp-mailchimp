# Mailchimp MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to Mailchimp Marketing API endpoints with OAuth authentication.

## Features

This MCP server provides the following Mailchimp operations:

### Automation Management

- **list_automations**: Get a summary of account's classic automations with filtering and pagination
- **get_automation_info**: Retrieve detailed information about a specific automation workflow
- **list_automated_emails**: Get emails in a classic automation workflow
- **get_workflow_email_info**: Get detailed information about a specific email in an automation
- **list_automated_email_subscribers**: Get subscribers queued for a specific automation email
- **get_automated_email_subscriber**: Get information about a specific subscriber in an automation queue

### Audience & List Management

- **list_audience**: Get information about all lists (audiences) in the account
- **get_list_info**: Retrieve details of a specific list with member statistics

### Campaign Management

- **list_campaigns**: Get all campaigns in the account
- **get_campaign_info**: Retrieve detailed information about a specific campaign

### Campaign Reports & Analytics

- **list_campaign_reports**: Get campaign reports with performance metrics
- **get_campaign_report**: Get detailed report for a specific sent campaign with opens, clicks, revenue

### Template Management

- **list_templates**: Get all email templates with filtering by type and content
- **get_template_info**: Retrieve details of a specific template
- **add_template**: Create a new Classic template with HTML (supports Mailchimp Template Language)
- **update_template**: Update template name, HTML, or folder location
- **list_template_folders**: Get all template folders
- **add_template_folder**: Create a new template folder for organization

### Landing Pages

- **list_landing_pages**: Get all landing pages with sorting options
- **get_landing_page_info**: Retrieve detailed information about a specific landing page
- **get_landing_page_content**: Get the HTML content of a landing page

### E-commerce Integration

- **list_stores**: Get information about all connected e-commerce stores
- **get_store_info**: Retrieve details of a specific store
- **list_products**: Get products from a specific store
- **get_product_info**: Retrieve detailed information about a specific product
- **list_store_orders**: Get orders from a specific store with filtering
- **get_order_info**: Retrieve complete details of a specific order

### Utility

- **health_check**: Check Mailchimp API connectivity

## Setup

### 1. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

### 2. Configure Mailchimp OAuth

You need to create a Mailchimp app with OAuth support:

1. Go to [Mailchimp Developer](https://us1.admin.mailchimp.com/account/oauth2/)
2. Register an application
3. Configure OAuth settings:
   - Add redirect URI for your application
   - Note your Client ID and Client Secret
4. Set required scopes for your integration

### 3. Get OAuth Token

After setting up OAuth, you'll receive an access token. You'll also need your server prefix (e.g., 'us18').

To find your server prefix:

1. Log into your Mailchimp account
2. Look at the URL: `https://us18.admin.mailchimp.com/...`
3. The server prefix is the part before `.admin.mailchimp.com` (e.g., `us18`)

## Usage Examples

### Health Check

```json
{
  "tool": "health_check",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18"
  }
}
```

### List Automations

```json
{
  "tool": "list_automations",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "count": 25,
    "status": "sending"
  }
}
```

### Get Campaign Report

```json
{
  "tool": "get_campaign_report",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "campaign_id": "abc123def"
  }
}
```

### Create Template

```json
{
  "tool": "add_template",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "name": "Welcome Email",
    "html": "<!DOCTYPE html><html><body><h1>Hello *|FNAME|*!</h1></body></html>",
    "folder_id": "folder123"
  }
}
```

### List Products from Store

```json
{
  "tool": "list_products",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "store_id": "store123",
    "count": 50
  }
}
```

### Query Orders by Campaign

```json
{
  "tool": "list_store_orders",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "store_id": "store123",
    "campaign_id": "campaign456",
    "count": 100
  }
}
```

### Update Template

```json
{
  "tool": "update_template",
  "arguments": {
    "oauth_token": "your_oauth_token",
    "server": "us18",
    "template_id": "11787417",
    "name": "Updated Welcome Email",
    "html": "<!DOCTYPE html><html>...updated HTML...</html>"
  }
}
```

## API Parameters

### Automation Status Filters

- `save` - Draft automations
- `paused` - Paused automations
- `sending` - Active automations

### Campaign Types

- `regular` - Regular campaigns
- `plaintext` - Plain text campaigns
- `absplit` - A/B split test campaigns
- `rss` - RSS campaigns
- `variate` - Multivariate campaigns

### Template Types

- `user` - User-created templates
- `base` - Built-in base templates
- `gallery` - Gallery templates

### Template Content Types

- `html` - Code your own HTML
- `template` - Legacy email editor templates
- `multichannel` - New editor templates

### Mailchimp Template Language (MTL) Tags

Common merge tags for templates:

- `*|FNAME|*` - Subscriber's first name
- `*|LNAME|*` - Subscriber's last name
- `*|EMAIL|*` - Subscriber's email
- `*|MC:SUBJECT|*` - Email subject line
- `*|ARCHIVE|*` - Link to archived version
- `*|UNSUB|*` - Unsubscribe link
- `*|UPDATE_PROFILE|*` - Update preferences link
- `*|LIST:DESCRIPTION|*` - List description
- `*|HTML:LIST_ADDRESS_HTML|*` - Company address
- `*|CURRENT_YEAR|*` - Current year

### Project Structure

```
mailchimp_mcp/
├── tools/
│   ├── __init__.py
│   ├── marketing_operations.py   # Automation, campaigns, lists, reports
│   └── template_operations.py    # Templates and folders
│   └── store_operations.py       #  store operations, orders, and products
├── utils/
│   └── mailchimp_utils.py        # client request utilities
├── mailchimp_mcp_server.py       # Main server file
├── requirements.txt              # Python dependencies
├── railway.json                  # Railway deployment config
└── README.md
```

## Deployment

### Railway Deployment

This server is configured for Railway deployment with `railway.json`:

```bash
# Deploy to Railway
railway up
```

The server will run on port 8080 using streamable-http transport.

### Environment Variables

For production deployment, you need to set on client side:

- `MAILCHIMP_CLIENT_ID` - Your Mailchimp OAuth client ID (optional)
- `MAILCHIMP_CLIENT_SECRET` - Your Mailchimp OAuth client secret (optional)

## Troubleshooting

### Authentication Errors

Ensure your OAuth token is valid:

1. Provide the access token
2. Verify you have the correct server prefix
3. Ensure required scopes are granted
4. Test with the `health_check` tool first

### Rate Limiting

Mailchimp API has rate limits (10 simultaneous connections):

- Reduce `count` parameters for large requests
- Add delays between bulk operations
- Monitor API usage in your Mailchimp account
- Check [Mailchimp API Status](https://status.mailchimp.com/)

### Template Creation Issues

If template creation fails:

- Ensure HTML is valid
- Check that MTL tags are correctly formatted
- Verify folder_id exists (if provided)
- Only Classic templates are supported (not drag-and-drop)

### Planned Features

- List Members Management
- Segments
- Tags
- Campaign Content
- Conversations
- File Manager

## Performance Tips

1. **Use pagination**: Set appropriate `count` and `offset` values
2. **Filter results**: Use specific filters to reduce data transfer
3. **Batch operations**: Group related API calls when possible
4. **Cache responses**: Cache frequently accessed data client-side
5. **Monitor limits**: Track your API usage in Mailchimp dashboard

## Resources

- [Mailchimp Marketing API Documentation](https://mailchimp.com/developer/marketing/api/)
