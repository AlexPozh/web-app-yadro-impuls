from typing import TYPE_CHECKING
import logging

from sqlalchemy.exc import DBAPIError

from app.utils.api_client import fetch_api_data
from app.utils.process_data import process_user_data
from .models.user import User
from .crud.user import create_users

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("development")

async def load_new_users(
    session: "AsyncSession",
    url: str
):
    try:
        raw_data = await fetch_api_data(url)
        processed_data = process_user_data(raw_data)
        await create_users(session, processed_data)
    except DBAPIError as e:
        logger.exception("Loading new users failed - %r", e)
        raise