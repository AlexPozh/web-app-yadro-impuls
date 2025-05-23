import logging
from typing import Any

import httpx

logger = logging.getLogger("development")

async def fetch_api_data(url: str) -> list[dict[str, Any]] | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status() # raise exception, if status code is not 2xx
            return response.json()["results"]
    except httpx.HTTPStatusError as e:
        logger.exception("Response error - %r", e)
        raise
    except httpx.RequestError as e:
        logger.exception("Request failed - %r", e)
        raise