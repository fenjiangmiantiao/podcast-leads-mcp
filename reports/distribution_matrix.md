# Distribution matrix — podcast-leads-mcp

Probed 2026-11-25 (America/Tijuana). Every row below was checked against the live page;
anything not reachable is marked **unconfirmed** rather than guessed.

## Summary

| Venue | Live page / evidence | Accepts new submissions? | What it needs | Cost | Can we finish it with no account? |
|---|---|---|---|---|---|
| **MCP Registry** (official) | `registry.modelcontextprotocol.io/v0/servers?search=podcast-leads-mcp` → 1 entry, `status=active`, `packages[0].registryType=mcpb` | ✅ already live | `mcp-publisher` + `server.json` + GitHub OAuth/PAT | free | ✅ done (published 2026-11-25T03:43Z) |
| **Glama** | page 200; clicked *Claim* → panel reads "Claim your MCP Server" / "Sign in with GitHub to claim" / "Sign in with GitHub so Glama can verify that you maintain this server" / "You don't have to do anything for your server to appear on this site, as we continuously fetch updates from GitHub" | listing auto-indexed ✅; **Claim = maintainer verification only** | Claim requires GitHub sign-in (OAuth). Indexing requires nothing. | none seen | ✅ already listed; ⚠️ claim needs the repo owner to sign in |
| **mcpservers.org** | `/submit` 200: "Listings on mcpservers.org are free"; fields = Server Name, Category, Short Description, Repository/Website/Docs, *Official MCP Registry Name* (optional), remote checkbox, Contact Email; Free $0 review ≤2 weeks, Premium $39 ≤24h | ✅ yes (free tier) | plain web form + an email address | $0 (paid $39 optional) | ⚠️ no account needed — but it is a form submission, so a human must click submit |
| **mcpmarket.com** | `/submit` 200: "Submit the related GitHub repository below and we'll review it for inclusion", fields = GitHub repo URL (+ remote MCP), "We'll email you the moment your listing goes live" | ✅ yes | GitHub repo URL + email | no price shown | ⚠️ form only, no account |
| **mcp.directory** | `/submit` 200: "We'll auto-pull metadata from GitHub and publish within 24 hours", fields = GitHub Repository URL* (+ optional npm/PyPI/short description/email) | ✅ yes | GitHub repo URL (npm/PyPI optional) | no price shown | ⚠️ form only, no account |
| **mcp.so** | `/submit` 200: "A paid listing is a one-time $39 fee: it is published immediately without review"; the whole page contains **zero** occurrences of "free" | ✅ paid only | Repository URL + Name, then $39 checkout ("Pay and submit automatically") | **$39 one-time** | ❌ needs payment (and a payer) |
| **PulseMCP** | `/submit` 200: "Apologies, submissions and changes are temporarily paused … We are not accepting new MCP server or client submissions right now"; `/servers/podcast-leads-mcp` → 404 | ❌ paused | — | — | ❌ dead end until they reopen |
| **Cline MCP Marketplace** | `github.com/cline/mcp-marketplace` README: submit via a new **GitHub issue** (`mcp-server-submission.yml`); needs GitHub repo URL, a **400×400 PNG logo**, a reason, and confirmation you tested setup with Cline | ✅ yes | GitHub account + issue + 400×400 icon | free | ❌ needs a GitHub issue from an account (we do not file issues) |
| **Cursor Directory** | `cursor.directory/plugins/new` → **429 Vercel Security Checkpoint** (bot wall) | **unconfirmed** | — | — | unconfirmed |
| **mcp-server-directory.com** | DNS resolves only to Clash fake-ip `198.18.0.222`; HTTPS fails on both apex and www (`http=000`, `schannel: server closed abruptly`) | **unconfirmed** | — | — | ❌ site unreachable / existence unconfirmed |
| **GitHub MCP Registry** (`github.com/mcp`) | real browser, searched `podcast-leads-mcp` → *"No MCPs found matching …"*. Its API `api.mcp.github.com/v0/servers?search=` ignores the query (returns the same 30 curated servers). | auto-ingest from the official registry (needs no submission) | nothing on our side | free | ⏳ not synced yet, ~1 h after publish; expected within 1–2 h — recheck later |
| **awesome-mcp-servers** (punkpeye) | `gh pr view 20584` → `state=OPEN`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN` | ✅ submitted | — | free | ✅ waiting on maintainer merge |
| **Smithery** | retired its proxy/hosting 2026-10-31, now a plain registry, submissions closed | ❌ | — | — | ❌ dead end |

### Verdicts

- **Already live, nothing to do:** official MCP Registry, Glama (auto-indexed).
- **Free, one form click, no account — worth doing by a human:** mcpservers.org, mcpmarket.com, mcp.directory.
- **Dead ends:** Smithery (closed), PulseMCP (submissions paused), mcp.so (paid $39 only), mcp-server-directory.com (unreachable), Cline (needs a GitHub issue), Cursor Directory (bot wall, unconfirmed), Glama *Claim* (owner OAuth — optional only).
- **Automatic follow-on:** GitHub MCP Registry / VS Code gallery ingest the official registry; recheck `github.com/mcp?search=podcast-leads-mcp` in a couple of hours.

## Ready-to-paste copy

### Long description (110 words)

podcast-leads-mcp is an MCP server that turns a keyword into podcast host emails, so an agent can run podcast outreach without any HTTP plumbing. Call `search_podcasts(query="fintech", require_email=true, active_within_days=90)` and you get leads with `primary_email`, website, recent episode titles and `days_since_last`, plus a `meta` funnel reporting how many candidates were dropped and why. Two real uses: prospecting fintech shows for a PR campaign, and enriching a sponsor list you already have via `enrich_podcasts` (RSS URLs or Apple collection ids in, the same lead shape out). Install with `uvx --from git+https://github.com/fenjiangmiantiao/podcast-leads-mcp podcast-leads-mcp`, or drag the `.mcpb` bundle into Claude Desktop. Free tier: 50 leads/month; empty results are never billed. MIT, Python.

### Short description (48 words)

Find podcast host emails by keyword — returns `primary_email`, website and activity signals, with a funnel explaining every dropped candidate. Also enriches RSS feeds or Apple IDs you already have. Free tier: 50 leads/month. Install: `uvx --from git+https://github.com/fenjiangmiantiao/podcast-leads-mcp podcast-leads-mcp`.

### Meta description (131 chars)

MCP server for podcast lead gen: keyword in, host emails plus activity signals out, with a transparent funnel. Free 50 leads/month.

### Tags

`mcp` `mcp-server` `model-context-protocol` `podcast` `podcast-marketing` `lead-generation` `email-finder` `prospecting` `claude` `cursor` `n8n` `python` `rapidapi`

## Links to paste

| Purpose | URL |
|---|---|
| Repository | https://github.com/fenjiangmiantiao/podcast-leads-mcp |
| Release page | https://github.com/fenjiangmiantiao/podcast-leads-mcp/releases/tag/v0.1.0 |
| Bundle asset (.mcpb, 3,427 B, sha256 `5dba2c45…7a8c`) | https://github.com/fenjiangmiantiao/podcast-leads-mcp/releases/download/v0.1.0/podcast-leads-mcp-0.1.0.mcpb |
| MCP Registry name | `io.github.fenjiangmiantiao/podcast-leads-mcp` |
| MCP Registry lookup | https://registry.modelcontextprotocol.io/v0/servers?search=podcast-leads-mcp |
| Glama listing | https://glama.ai/mcp/servers/fenjiangmiantiao/podcast-leads-mcp |
| awesome-mcp-servers PR | https://github.com/punkpeye/awesome-mcp-servers/pull/20584 |
| RapidAPI subscribe (needed for a key) | https://rapidapi.com/JaneThompson/api/podcast-leads-api |
## Submission results (2026-11-25, submitted by main session)

| Venue | Result | Detail |
|---|---|---|
| mcpservers.org | ✅ **submitted** | Free tier, "Submission Successful", review within 2 weeks, email notification on approval. Category: Marketing. Registry name included. |
| mcp.directory | ✅ **submitted** | "Server Submitted!", auto-pull from GitHub, publish within 24 hours. |
| mcpmarket.com | ❌ **paid** | The submit button redirects to a Stripe checkout: **USD 29.00 one-time** (SGD 38.97). Not a free listing — the earlier "no price shown" reading was wrong; price only appears at checkout. Not paid. |
| mcp.so | ⏸ not paid | USD 39 one-time, paid-only listing. |
| Glama Claim | ⏸ skipped | Needs GitHub OAuth sign-in; listing is already live without claiming. |

Pending: 2h recheck of github.com/mcp auto-ingest.