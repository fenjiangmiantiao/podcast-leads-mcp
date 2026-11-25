# Container image for the podcast-leads MCP server.
# MCP speaks JSON-RPC over stdio, so there is no port to expose and no healthcheck to hit.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Metadata files first: hatchling reads README.md and LICENSE while building the wheel.
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir .

# The key is supplied at run time by the MCP client, e.g.
#   docker run -i --rm -e PODCAST_LEADS_RAPIDAPI_KEY=... podcast-leads-mcp
CMD ["python", "-m", "podcast_leads_mcp.server"]
