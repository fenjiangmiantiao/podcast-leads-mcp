"""podcast-leads-mcp - MCP server for the Podcast Leads API on RapidAPI.

Exposes two tools so any MCP client (Claude Desktop, Cursor, n8n, ...) can find
podcast host emails without writing HTTP code.

The API bills per lead returned, not per call: dead feeds and empty results are free.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

HOST = "podcast-leads-api.p.rapidapi.com"
DEFAULT_BASE_URL = f"https://{HOST}"
TIMEOUT_SECS = 90.0

# Escape hatches for self-hosted deployments and local debugging:
#   PODCAST_LEADS_BASE_URL      point at your own copy (e.g. a Fly.io app)
#   PODCAST_LEADS_PROXY_SECRET  talk to the backend directly instead of via RapidAPI
BASE_URL = os.getenv("PODCAST_LEADS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
PROXY_SECRET = os.getenv("PODCAST_LEADS_PROXY_SECRET", "").strip()

mcp = FastMCP("podcast-leads")


def _api_key() -> str:
    key = os.getenv("PODCAST_LEADS_RAPIDAPI_KEY", "").strip()
    if not key:
        raise ToolError(
            "PODCAST_LEADS_RAPIDAPI_KEY is not set. Subscribe at "
            "https://rapidapi.com/JaneThompson/api/podcast-leads-api and copy your "
            "X-RapidAPI-Key."
        )
    return key


async def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    if PROXY_SECRET:
        headers = {
            "X-RapidAPI-Proxy-Secret": PROXY_SECRET,
            "Content-Type": "application/json",
        }
    else:
        headers = {
            "X-RapidAPI-Key": _api_key(),
            "X-RapidAPI-Host": HOST,
            "Content-Type": "application/json",
        }
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECS, trust_env=True) as client:
            response = await client.post(f"{BASE_URL}{path}", json=payload, headers=headers)
    except httpx.HTTPError as exc:
        raise ToolError(
            f"Network error calling {BASE_URL}{path}: {type(exc).__name__}: {exc}"
        ) from exc
    if response.status_code >= 400:
        raise ToolError(_describe_error(response))
    return response.json()


def _describe_error(response: httpx.Response) -> str:
    """Turn the RapidAPI error envelope into something a human can act on."""
    try:
        body = response.json()
    except ValueError:
        return f"HTTP {response.status_code}: {response.text[:200]}"
    message = body.get("message") or body.get("error") or response.text[:200]
    hint = ""
    if response.status_code in (401, 403):
        hint = " Check that you subscribed to the API and that the key is current."
    elif response.status_code == 429:
        hint = " You hit the plan monthly lead quota; upgrade or wait for the reset."
    return f"HTTP {response.status_code}: {message}{hint}"


@mcp.tool()
async def search_podcasts(
    query: str,
    limit: int = 10,
    require_email: bool = True,
    active_within_days: int = 90,
    country: str = "us",
) -> dict[str, Any]:
    """Find podcasts by keyword and return host contact details.

    Args:
        query: Keyword or niche, e.g. "fintech", "B2B sales", "cybersecurity".
        limit: How many leads to return (1-50).
        require_email: Only return shows where a host email was found.
        active_within_days: Drop shows whose last episode is older than this.
        country: Two-letter storefront code used for discovery.

    Returns a leads array (one object per podcast: primary_email, emails,
    website, days_since_last, language, recent_episode_titles, social_links, ...)
    plus a meta funnel block explaining how many candidates were dropped and why.
    """
    return await _post(
        "/v1/podcasts/search",
        {
            "query": query,
            "limit": max(1, min(50, limit)),
            "requireEmail": require_email,
            "activeWithinDays": max(0, active_within_days),
            "country": country.lower()[:2],
        },
    )


@mcp.tool()
async def enrich_podcasts(
    feed_urls: list[str] | None = None,
    apple_ids: list[int] | None = None,
    require_email: bool = False,
) -> dict[str, Any]:
    """Enrich podcast feeds you already have into the same lead shape.

    Args:
        feed_urls: RSS feed URLs, up to 20 per call.
        apple_ids: Apple Podcasts collection ids, up to 20 per call (resolved to feeds).
        require_email: Drop shows without a host email.

    Use this for CRM enrichment: you have a list of shows, you want emails and
    activity signals back.
    """
    if not feed_urls and not apple_ids:
        raise ValueError("Pass at least one of feed_urls or apple_ids.")
    return await _post(
        "/v1/podcasts/enrich",
        {
            "feedUrls": (feed_urls or [])[:20],
            "appleIds": (apple_ids or [])[:20],
            "requireEmail": require_email,
        },
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
