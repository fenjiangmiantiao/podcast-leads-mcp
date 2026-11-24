# podcast-leads-mcp

An MCP server for the [Podcast Leads API](https://rapidapi.com/JaneThompson/api/podcast-leads-api).
Give Claude, Cursor, or n8n a keyword and it comes back with podcast host emails, websites,
and activity signals — no HTTP plumbing in your prompt.

```
"Find active fintech podcasts with a host email I can pitch"
  -> search_podcasts(query="fintech", require_email=true, active_within_days=90)
  -> 10 leads: primary_email, website, days_since_last, recent_episode_titles, ...
```

## Why this exists

Most "podcast contact" lists are dead shows and `noreply@libsyn.com` aliases. This API reads the
RSS head only (never the whole feed), filters hosting-platform aliases, and reports how many
candidates it dropped and why. You pay per lead returned, not per call — empty results are free.

## Install

```bash
# zero-install, if you have uv
uvx --from git+https://github.com/fenjiangmiantiao/podcast-leads-mcp podcast-leads-mcp

# or the classic way
pip install git+https://github.com/fenjiangmiantiao/podcast-leads-mcp
```

Get a key first: subscribe to the free BASIC plan on
[RapidAPI](https://rapidapi.com/JaneThompson/api/podcast-leads-api) (50 leads/month, no card)
and copy your `X-RapidAPI-Key`.

```bash
export PODCAST_LEADS_RAPIDAPI_KEY=your_key_here
```

## Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "podcast-leads": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/fenjiangmiantiao/podcast-leads-mcp", "podcast-leads-mcp"],
      "env": { "PODCAST_LEADS_RAPIDAPI_KEY": "your_key_here" }
    }
  }
}
```

## Cursor

`.cursor/mcp.json` in your project, same shape as above.

## Tools

### `search_podcasts`

| arg | type | default | meaning |
|---|---|---|---|
| `query` | string | required | keyword or niche ("fintech", "B2B sales") |
| `limit` | int | 10 | leads to return, 1-50 |
| `require_email` | bool | true | only shows where a host email was found |
| `active_within_days` | int | 90 | drop shows whose last episode is older than this |
| `country` | string | "us" | two-letter storefront code for discovery |

Returns `leads[]` plus `meta` (funnel counters: discovered → scanned → returned, and
`filtered_out` with reasons like `no_email` / `inactive` / `rss_error`).

### `enrich_podcasts`

| arg | type | meaning |
|---|---|---|
| `feed_urls` | string[] | RSS URLs, up to 20 |
| `apple_ids` | int[] | Apple Podcasts collection ids, up to 20 |
| `require_email` | bool | drop shows without an email |

Use it when you already have a sponsor/guest list and want emails + activity back.

## Billing

- Pay per **lead returned**, not per request.
- Dead feeds, 404s, robots-blocked show pages and empty keywords cost nothing.
- Free tier: 50 leads/month. Paid tiers start at $19.

## Development

```bash
uv sync
uv run podcast-leads-mcp      # speaks MCP over stdio
```

## License

MIT
