import logging
from typing import TYPE_CHECKING

from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError

from .models.user import User

logger = logging.getLogger("development")

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    
async def get_total_users(session: "AsyncSession"):
    try:
        stmt = select(func.count(User.id))
        result = await session.execute(stmt)
        return result.scalar()
    except DBAPIError as e:
        logger.exception("Database selecting operation failed- %r", e)
        raise