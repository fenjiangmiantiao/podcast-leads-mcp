# podcast-leads-mcp

An MCP server for the [Podcast Leads API](https://rapidapi.com/JaneThompson/api/podcast-leads-api).
Give Claude, Cursor, or n8n a keyword and it comes back with podcast host emails, websites,
and activity signals — no HTTP plumbing in your prompt.

> **You need an API key — the MCP package is only the client.**
> Free BASIC plan: 50 leads/month, no card →
> **[Subscribe on RapidAPI](https://rapidapi.com/JaneThompson/api/podcast-leads-api)**, then copy your `X-RapidAPI-Key`.
> Installing this package on your own machine does not remove that requirement.

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

## Example output

A real `search_podcasts(query="AI SaaS", limit=10)` response, trimmed for width: three of
the returned leads, contact emails masked as `ed***@changelog.com`, and the
`recent_episode_titles` / `social_links` lists dropped.

```json
{
  "query": "AI SaaS",
  "country": "us",
  "requested": 10,
  "scanned": 10,
  "returned": 3,
  "bills_leads": 3,
  "duration_ms": 2023,
  "sources": ["podcast_index"],
  "meta": {
    "requested": 10,
    "discovered": 10,
    "scanned": 10,
    "returned": 3,
    "billed_leads": 3,
    "filtered_out": { "no_email": 4, "inactive": 3 },
    "oversampled": false,
    "note": "\"limit\" is the maximum number of leads returned; filtered_out explains the rest."
  },
  "leads": [
    {
      "title": "The Changelog: Software Development, Open Source",
      "artist": "The Changelog",
      "feed_url": "https://changelog.com/podcast/feed",
      "website": "https://changelog.com/podcast",
      "owner_name": "Changelog Media",
      "emails": ["ed***@changelog.com"],
      "primary_email": "ed***@changelog.com",
      "days_since_last": 3,
      "is_active_90d": true,
      "episodes_per_month": 6.09,
      "track_count": 5,
      "rss_status": 200,
      "rss_bytes_read": 33306,
      "rss_truncated": true,
      "error": null
    },
    {
      "title": "Darknet Diaries",
      "artist": "Darknet Diaries",
      "feed_url": "https://feeds.megaphone.fm/darknetdiaries",
      "website": "https://darknetdiaries.com/",
      "owner_name": "Jack Rhysider",
      "emails": ["po***@darknetdiaries.com"],
      "primary_email": "po***@darknetdiaries.com",
      "days_since_last": 20,
      "is_active_90d": true,
      "episodes_per_month": 2.23,
      "track_count": 5,
      "rss_status": 200,
      "rss_bytes_read": 139043,
      "rss_truncated": true,
      "error": null
    },
    {
      "title": "Security Now (Audio)",
      "artist": "Security Now (TWiT)",
      "feed_url": "https://feeds.twit.tv/sn.xml",
      "website": "https://twit.tv/shows/security-now",
      "owner_name": "Leo Laporte",
      "emails": ["fe***@twit.tv"],
      "primary_email": "fe***@twit.tv",
      "days_since_last": 6,
      "is_active_90d": true,
      "episodes_per_month": 4.35,
      "track_count": 5,
      "rss_status": 200,
      "rss_bytes_read": 160299,
      "rss_truncated": true,
      "error": null
    }
  ]
}
```

The `meta` block is the whole point: `scanned: 10` became `returned: 3` because four shows
had no host email and three had gone quiet. Nothing is hidden and nothing is billed for the
seven you did not get.

## Billing

- Pay per **lead returned**, not per request.
- Dead feeds, 404s, robots-blocked show pages and empty keywords cost nothing.
- Free tier: 50 leads/month. Paid tiers start at $19.

## Troubleshooting

Errors surface as tool errors with a hint, never as stack traces.

| Symptom | What you see | Fix |
|---|---|---|
| `401` / `403` | `HTTP 403: ... Check that you subscribed to the API and that the key is current.` | The key is stale or the RapidAPI app is not subscribed. Re-copy `X-RapidAPI-Key` from the API's **Endpoints** tab; the free BASIC plan is enough. |
| `429` | `HTTP 429: ... You hit the plan monthly lead quota; upgrade or wait for the reset.` | The monthly *lead* quota is spent (50 on BASIC). Requests stay free — only returned leads count. Wait for the reset or upgrade. |
| `PODCAST_LEADS_RAPIDAPI_KEY is not set` | Raised before any HTTP call | The env var is missing from the MCP client config. Claude Desktop and Cursor only inherit what you put in the `env` block. |
| `Network error calling ...` | `ConnectError` / `ReadTimeout` | Egress is blocked or a proxy is in the way. The server honours standard proxy env vars (`HTTPS_PROXY`); raise `PODCAST_LEADS_BASE_URL` to a self-hosted copy if the gateway is unreachable. |
| `leads: []` with a `meta.filtered_out` map | `{"no_email": 8, "inactive": 2}` | Not a failure. Try a broader keyword, set `require_email: false` to see shows without a contact, or raise `active_within_days` past 90. Empty results are never billed. |

## Development

```bash
uv sync
uv run podcast-leads-mcp      # speaks MCP over stdio
```

## MCP Registry

Published as [`io.github.fenjiangmiantiao/podcast-leads-mcp`](https://registry.modelcontextprotocol.io/v0/servers?search=podcast-leads-mcp)
— version 0.1.0, `mcpb` package, stdio transport.

**Install the bundle.** Grab [`podcast-leads-mcp-0.1.0.mcpb`](https://github.com/fenjiangmiantiao/podcast-leads-mcp/releases/download/v0.1.0/podcast-leads-mcp-0.1.0.mcpb)
and open it with an MCPB-aware client (Claude Desktop: drag it in). The bundle runs on the uv runtime
and pulls `mcp<2` + `httpx` on first launch. Set `PODCAST_LEADS_RAPIDAPI_KEY` in the client's
environment — the registry entry marks it required and secret.

Built from `manifest.json` + `mcpb/pyproject.toml`; `server.json` is the registry descriptor.
Maintainers republish with the [`mcp-publisher`](https://github.com/modelcontextprotocol/registry) CLI:

```bash
npx @anthropic-ai/mcpb pack mcpb-build podcast-leads-mcp-0.1.0.mcpb   # then attach to a GitHub release
mcp-publisher validate        # schema + semantic checks, no login required
mcp-publisher login github    # OAuth device flow, or --token <PAT> with read:org
mcp-publisher publish
```

## Where to find it

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/fenjiangmiantiao/podcast-leads-mcp)

- **MCP Registry** — [`io.github.fenjiangmiantiao/podcast-leads-mcp`](https://registry.modelcontextprotocol.io/v0/servers?search=podcast-leads-mcp), published 2026-11-25, `mcpb` package.
- **mcpservers.org** — [approved listing](https://mcpservers.org/servers/fenjiangmiantiao/podcast-leads-mcp), live 2026-11-25.
- **Glama** — [quality-scored listing](https://glama.ai/mcp/servers/fenjiangmiantiao/podcast-leads-mcp) (auto-indexed from GitHub).
- **awesome-mcp-servers** — [PR #20584](https://github.com/punkpeye/awesome-mcp-servers/pull/20584), open and waiting on the maintainer.

## License

MIT
