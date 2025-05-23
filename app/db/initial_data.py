from typing import TYPE_CHECKING, AsyncGenerator
import logging

from sqlalchemy import select, exists
from sqlalchemy.exc import DBAPIError
import httpx

from app.utils.api_client import fetch_api_data
from app.utils.process_data import process_user_data
from .models.user import User
from .crud.user import create_users

logger = logging.getLogger("development")

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

_URL = "https://randomuser.me/api/?inc=gender,name,email,phone,location,picture&results=1000"

async def initialize_users(
    session_gen: AsyncGenerator["AsyncSession", None]
):
    try:
        s = await anext(session_gen)
        if await _is_db_empty(s):
            raw_data = await fetch_api_data(_URL)
            processed_data = process_user_data(raw_data)
            await create_users(s, processed_data)
        else:
            logger.info("Database already exists data")
    except DBAPIError as e:
        logger.exception("Database initializing failed", e)
    except httpx.HTTPStatusError as e:
        logger.exception("Response error, initializing failed - %r", e)
    except httpx.RequestError as e:
        logger.exception("Request failed, initializing failed - %r", e)

async def _is_db_empty(
    session: "AsyncSession"
) -> bool:
    stmt = select(exists().where(User.id.is_not(None)))
    result = await session.scalar(stmt)
    return not result
