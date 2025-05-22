from typing import TYPE_CHECKING
import logging

from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError, NoResultFound

from app.schemas.user import CreateUserDB, GetUserDB
from app.db.models.user import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("development")

async def create_users(
    session: "AsyncSession",
    users_data: list[CreateUserDB]
) -> None:
    try:
        users = [User(**user_data.model_dump()) for user_data in users_data]
        session.add_all(users)
    except DBAPIError as e:
        await session.rollback()
        logger.exception("Database operation is failed - %r", e)
        raise
    else:
        await session.commit()
        logger.info("Users added successfully")


async def get_users(
    session: "AsyncSession",
    limit: int = 10,
    offset: int = 0
) -> list[GetUserDB] | None:
    try:
        stmt = select(User).limit(limit).offset(offset)
        result = await session.execute(stmt)
        users = result.all()
        return [
            GetUserDB(
                id=user[0].id,
                gender=user[0].gender,
                name=user[0].name,
                surname=user[0].surname,
                phone_number=user[0].phone_number,
                email=user[0].email,
                country=user[0].country,
                state=user[0].state,
                city=user[0].city,
                street=user[0].street,
                photo_url=user[0].photo_url
            ) for user in users
        ]
    except DBAPIError as e:
        logger.exception("Database operation is failed - %r", e)
        raise
    except NoResultFound:
        return []
    

async def get_user(
    session: "AsyncSession",
    user_id: int
) -> User | None:
    try:
        stmt = select(User).where(User.id==user_id)
        user = await session.scalar(stmt)
        return user
    except DBAPIError as e:
        logger.exception("Database operation is failed - %r", e)
        raise


async def get_random_user(
    session: "AsyncSession"
) -> User | None:
    try:
        stmt = select(User).order_by(func.random()).limit(limit=1)
        user = await session.scalar(stmt)
        return user
    except DBAPIError as e:
        logger.exception("Database operation is failed - %r", e)
        raise