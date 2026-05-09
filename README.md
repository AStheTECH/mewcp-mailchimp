**Your Mailchimp account, fully accessible through AI.**

A Model Context Protocol (MCP) server that exposes Mailchimp's Marketing API for managing campaigns, automations, audiences, templates, landing pages, and e-commerce data.


## Overview

The Mailchimp MCP Server provides a complete interface to your Mailchimp account:

- Manage classic automations, workflows, and subscriber queues
- Create, update, and retrieve campaigns, templates, and landing pages
- Access e-commerce stores, products, and orders with full reporting

Perfect for:

- AI assistants that need to read or manage Mailchimp marketing data
- Automating campaign analysis and performance reporting
- Building tools that integrate Mailchimp with other services


## Tools

<details>
<summary><code>health_check</code> — Check Mailchimp API connectivity</summary>

Pings the Mailchimp API to verify credentials and connectivity are working correctly.

**Inputs:**
```
None
```

**Output:**

```json
{
  "health_status": "Everything's Chimpy!"
}
```

</details>


<details>
<summary><code>list_automations</code> — List all classic automation workflows</summary>

Returns a paginated summary of all classic automations in the account, with optional filtering by status or date range.

**Inputs:**
```
- `count` (int, optional) — Number of records to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
- `fields` (string, optional) — Comma-separated list of fields to return
- `exclude_fields` (string, optional) — Comma-separated list of fields to exclude
- `before_create_time` (string, optional) — ISO 8601 datetime; restrict to automations created before this time
- `since_create_time` (string, optional) — ISO 8601 datetime; restrict to automations created after this time
- `before_start_time` (string, optional) — ISO 8601 datetime; restrict to automations started before this time
- `since_start_time` (string, optional) — ISO 8601 datetime; restrict to automations started after this time
- `status` (string, optional) — Filter by status: `save`, `paused`, or `sending`
```

**Output:**

```json
{
  "automations": [...],
  "total_items": 5
}
```

</details>


<details>
<summary><code>get_automation_info</code> — Get details of a specific automation workflow</summary>

Returns full details of a single automation workflow including settings, tracking, and status.

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the automation workflow
- `fields` (string, optional) — Comma-separated list of fields to return
- `exclude_fields` (string, optional) — Comma-separated list of fields to exclude
```

**Output:**

```json
{
  "id": "b0a1c24f6b",
  "status": "sending",
  "emails_sent": 120,
  ...
}
```

</details>


<details>
<summary><code>list_automated_emails</code> — List emails in an automation workflow</summary>

Returns a summary of all emails configured within a specific classic automation workflow.

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the automation workflow
```

**Output:**

```json
{
  "emails": [...],
  "total_items": 3
}
```

</details>


<details>
<summary><code>get_workflow_email_info</code> — Get details of a specific automation email</summary>

Returns detailed information about one email step within an automation workflow, including delay settings, content, tracking, and performance metrics.

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the automation workflow
- `workflow_email_id` (string, required) — The unique ID of the automation workflow email
```

**Output:**

```json
{
  "id": "a1b2c3d4e5",
  "subject_line": "Welcome!",
  "status": "sending",
  "open_rate": 0.42,
  ...
}
```

</details>


<details>
<summary><code>list_automated_email_subscribers</code> — List subscribers queued for an automation email</summary>

Returns the list of subscribers currently queued to receive a specific automation email.

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the automation workflow
- `workflow_email_id` (string, required) — The unique ID of the automation workflow email
```

**Output:**

```json
{
  "queue": [...],
  "total_items": 15
}
```

</details>


<details>
<summary><code>get_automated_email_subscriber</code> — Get a specific subscriber in an automation email queue</summary>

Returns details about a specific subscriber's position in an automation email queue.

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the automation workflow
- `workflow_email_id` (string, required) — The unique ID of the automation workflow email
- `subscriber_hash` (string, required) — MD5 hash of the lowercase subscriber email address
```

**Output:**

```json
{
  "id": "subscriber_hash",
  "email_address": "user@example.com",
  "next_send": "2024-01-15T10:00:00+00:00"
}
```

</details>


<details>
<summary><code>list_audience</code> — List all audiences (lists)</summary>

Returns information about all lists (audiences) in the Mailchimp account.

**Inputs:**
```
None
```

**Output:**

```json
{
  "lists": [...],
  "total_items": 3
}
```

</details>


<details>
<summary><code>get_list_info</code> — Get details of a specific audience</summary>

Returns full details about a specific Mailchimp list including stats, settings, and contact defaults.

**Inputs:**
```
- `list_id` (string, required) — The unique ID for the list
```

**Output:**

```json
{
  "id": "a1b2c3d4e5",
  "name": "My Audience",
  "stats": { "member_count": 1200, ... },
  ...
}
```

</details>


<details>
<summary><code>list_campaigns</code> — List all campaigns</summary>

Returns all campaigns in the Mailchimp account.

**Inputs:**
```
None
```

**Output:**

```json
{
  "campaigns": [...],
  "total_items": 10
}
```

</details>


<details>
<summary><code>get_campaign_info</code> — Get details of a specific campaign</summary>

Returns full details about a specific campaign including settings, content, and status.

**Inputs:**
```
- `campaign_id` (string, required) — The unique ID for the campaign
```

**Output:**

```json
{
  "id": "campaign_id",
  "status": "sent",
  "subject_line": "Newsletter #42",
  ...
}
```

</details>


<details>
<summary><code>list_template_folders</code> — List all template folders</summary>

Returns all folders used to organize templates in the account.

**Inputs:**
```
- `count` (int, optional) — Number of folders to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
```

**Output:**

```json
{
  "folders": [...],
  "total_items": 4
}
```

</details>


<details>
<summary><code>add_template_folder</code> — Create a new template folder</summary>

Creates a new folder for organizing templates in the account.

**Inputs:**
```
- `name` (string, required) — The name of the folder
```

**Output:**

```json
{
  "id": "folder_id",
  "name": "My Folder",
  "count": 0
}
```

</details>


<details>
<summary><code>list_templates</code> — List all templates</summary>

Returns all templates in the account with optional filtering by type or content type.

**Inputs:**
```
- `count` (int, optional) — Number of templates to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
- `type` (string, optional) — Filter by type: `user`, `base`, or `gallery`
- `content_type` (string, optional) — Filter by content type: `html`, `template`, or `multichannel`
```

**Output:**

```json
{
  "templates": [...],
  "total_items": 8
}
```

</details>


<details>
<summary><code>get_template_info</code> — Get details of a specific template</summary>

Returns full details about a specific template including its name, type, and folder.

**Inputs:**
```
- `template_id` (string, required) — The unique ID for the template
```

**Output:**

```json
{
  "id": "template_id",
  "name": "My Template",
  "type": "user",
  ...
}
```

</details>


<details>
<summary><code>add_template</code> — Create a new template</summary>

Creates a new Classic template with custom HTML. Supports Mailchimp Template Language for dynamic content.

**Inputs:**
```
- `name` (string, required) — The name of the template
- `html` (string, required) — Raw HTML for the template; supports Mailchimp Template Language
- `folder_id` (string, optional) — The ID of the folder to place the template in
```

**Output:**

```json
{
  "id": "template_id",
  "name": "My Template",
  "type": "user"
}
```

</details>


<details>
<summary><code>update_template</code> — Update an existing template</summary>

Updates the name, HTML content, or folder of an existing template.

**Inputs:**
```
- `template_id` (string, required) — The unique ID for the template
- `name` (string, required) — The updated name of the template
- `html` (string, required) — Updated raw HTML; supports Mailchimp Template Language
- `folder_id` (string, optional) — The ID of the folder to move the template to
```

**Output:**

```json
{
  "id": "template_id",
  "name": "Updated Template",
  "type": "user"
}
```

</details>


<details>
<summary><code>list_campaign_reports</code> — List all campaign reports</summary>

Returns performance reports for all campaigns with optional filtering by campaign type.

**Inputs:**
```
- `count` (int, optional) — Number of reports to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
- `type` (string, optional) — Filter by campaign type: `regular`, `plaintext`, `absplit`, `rss`, or `variate`
```

**Output:**

```json
{
  "reports": [...],
  "total_items": 6
}
```

</details>


<details>
<summary><code>get_campaign_report</code> — Get report for a specific campaign</summary>

Returns the detailed performance report for a specific sent campaign including opens, clicks, and unsubscribes.

**Inputs:**
```
- `campaign_id` (string, required) — The unique ID for the campaign
```

**Output:**

```json
{
  "id": "campaign_id",
  "opens": { "opens_total": 450, "unique_opens": 300 },
  "clicks": { "clicks_total": 120, "unique_clicks": 95 },
  ...
}
```

</details>


<details>
<summary><code>list_landing_pages</code> — List all landing pages</summary>

Returns all landing pages in the account with optional sorting.

**Inputs:**
```
- `count` (int, optional) — Number of landing pages to return (default: 10, max: 1000)
- `sort_field` (string, optional) — Sort by: `created_at` or `updated_at`
- `sort_dir` (string, optional) — Sort direction: `ASC` or `DESC`
```

**Output:**

```json
{
  "landing_pages": [...],
  "total_items": 2
}
```

</details>


<details>
<summary><code>get_landing_page_info</code> — Get details of a specific landing page</summary>

Returns full information about a specific landing page including its status, URL, and settings.

**Inputs:**
```
- `page_id` (string, required) — The unique ID for the landing page
```

**Output:**

```json
{
  "id": "page_id",
  "name": "Spring Sale",
  "status": "published",
  "url": "https://mailchimp.com/landing/...",
  ...
}
```

</details>


<details>
<summary><code>get_landing_page_content</code> — Get the HTML content of a landing page</summary>

Returns the raw HTML content of a specific landing page.

**Inputs:**
```
- `page_id` (string, required) — The unique ID for the landing page
```

**Output:**

```json
{
  "html": "<!DOCTYPE html>..."
}
```

</details>


<details>
<summary><code>list_stores</code> — List all e-commerce stores</summary>

Returns all connected e-commerce stores in the Mailchimp account.

**Inputs:**
```
- `count` (int, optional) — Number of stores to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
```

**Output:**

```json
{
  "stores": [...],
  "total_items": 1
}
```

</details>


<details>
<summary><code>get_store_info</code> — Get details of a specific e-commerce store</summary>

Returns full details about a specific connected e-commerce store.

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
```

**Output:**

```json
{
  "id": "store_id",
  "name": "My Shop",
  "domain": "myshop.com",
  ...
}
```

</details>


<details>
<summary><code>list_products</code> — List products in an e-commerce store</summary>

Returns all products in a specific connected e-commerce store.

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `count` (int, optional) — Number of products to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
```

**Output:**

```json
{
  "products": [...],
  "total_items": 25
}
```

</details>


<details>
<summary><code>get_product_info</code> — Get details of a specific product</summary>

Returns full details about a specific product in an e-commerce store.

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `product_id` (string, required) — The unique ID for the product
```

**Output:**

```json
{
  "id": "product_id",
  "title": "Blue T-Shirt",
  "variants": [...],
  ...
}
```

</details>


<details>
<summary><code>list_store_orders</code> — List orders in an e-commerce store</summary>

Returns all orders in a specific e-commerce store with optional filtering by customer or campaign.

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `count` (int, optional) — Number of orders to return (default: 10, max: 1000)
- `offset` (int, optional) — Number of records to skip for pagination (default: 0)
- `customer_id` (string, optional) — Filter orders by a specific customer ID
- `campaign_id` (string, optional) — Filter orders attributed to a specific campaign ID
```

**Output:**

```json
{
  "orders": [...],
  "total_items": 42
}
```

</details>


<details>
<summary><code>get_order_info</code> — Get details of a specific order</summary>

Returns full details about a specific order in an e-commerce store including line items and customer info.

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `order_id` (string, required) — The unique ID for the order
```

**Output:**

```json
{
  "id": "order_id",
  "customer": { "email_address": "buyer@example.com" },
  "order_total": 59.99,
  "lines": [...],
  ...
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Pagination Parameters</strong></summary>

- `count` — Number of records to return per request (default: 10, max: 1000)
- `offset` — Number of records to skip; use with `count` to page through results

</details>

<details>
<summary><strong>Field Filtering</strong></summary>

- `fields` — Comma-separated list of response fields to include (reduces payload size)
- `exclude_fields` — Comma-separated list of response fields to omit

**Example:**
```
fields: "id,status,subject_line"
exclude_fields: "_links"
```

</details>

<details>
<summary><strong>Date/Time Format</strong></summary>

All datetime parameters use ISO 8601 format:

```
Format: YYYY-MM-DDTHH:MM:SS+HH:MM
Example: 2024-01-15T10:30:00+00:00
```

</details>

<details>
<summary><strong>Subscriber Hash</strong></summary>

The `subscriber_hash` parameter is the MD5 hash of the subscriber's lowercase email address.

```
Input: user@example.com → lowercase → user@example.com
Hash: md5("user@example.com") → b58996c504c5638798eb6b511e6f49af
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** Credentials not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that your Mailchimp OAuth credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Mailchimp credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Mailchimp account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values (e.g. `count` must be an integer)

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Mailchimp API Error</strong></summary>

- **Cause:** Upstream Mailchimp API returned an error
- **Solution:**
  1. Check Mailchimp service status at [Mailchimp Status Page](https://status.mailchimp.com)
  2. Verify your OAuth credential has the required permissions for the requested resource
  3. Review the error message returned in the response for specific details

</details>

---

### Resources

- **[Mailchimp Marketing API Documentation](https://mailchimp.com/developer/marketing/docs/fundamentals/)** — Official API reference
- **[Mailchimp API Reference](https://mailchimp.com/developer/marketing/api/)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling
