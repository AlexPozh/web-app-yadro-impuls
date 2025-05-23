from typing import TYPE_CHECKING, Annotated
import logging

from fastapi import APIRouter, Depends, Request, HTTPException, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import DBAPIError

from app.db.count_users import get_total_users
from app.db.load_new_users import load_new_users
from app.utils.templates import templates
from app.db.db_manager import db_manager
from app.db.crud.user import get_random_user, get_users, get_user

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("development")

router = APIRouter(
    prefix="/homepage",
    tags=["Users"]
)

_URL = "https://randomuser.me/api/?inc=gender,name,email,phone,location,picture&results={}"


@router.get("")
async def get_main_page(
    request: Request,
    page: int = 1,
    size: int = 20,
    session: "AsyncSession" = Depends(db_manager.session_getter)
):
    try:
        total_users = await get_total_users(session)
        total_pages = (total_users // size) + 1 # if total_users is None -> raise TypeError
        users = await get_users(session=session, limit=size, offset=(page - 1) * size)
        if users is None:
            raise HTTPException(status_code=404, detail="Users not found")
        
        return templates.TemplateResponse(
            name="index.html",
            request=request,
            context={
                "users": users,
                "page": page,
                "size": size,
                "total_page": total_pages
            }
        )
    except DBAPIError as e:
        logger.error("Database error: %r", e)
        raise HTTPException(status_code=500, detail="Internal server error")

    except TypeError as e:
        logger.error("Database error: %r", e)
        raise HTTPException(status_code=404, detail="Users not found")

@router.get("/random")
async def get_user_by_random(
    request: Request,
    session: "AsyncSession" = Depends(db_manager.session_getter)
):
    try:
        user = await get_random_user(
            session=session
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return templates.TemplateResponse(
            name="user.html",
            request=request,
            context={
                "user": user,
                "location": ", ".join([user.country, user.city, user.state, user.street])
            }
        )
    except DBAPIError as e:
        logger.error("Database error: %r", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    request: Request,
    session: "AsyncSession" = Depends(db_manager.session_getter)
):
    try:
        user = await get_user(
            session=session,
            user_id=user_id
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return templates.TemplateResponse(
            name="user.html",
            request=request,
            context={
                "user": user,
                "location": ", ".join([user.country, user.city, user.state, user.street])
            }
        )
    except DBAPIError as e:
        logger.error("Database error: %r", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/load_users")
async def post_new_users(
    count: Annotated[str, Form()],
    session: "AsyncSession" = Depends(db_manager.session_getter)
):
    try:
        await load_new_users(session, _URL.format(count))

        return RedirectResponse(
            url="/homepage",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except DBAPIError as e:
        logger.exception("Database opetaion is failed - %r", e)
        raise HTTPException(status_code=500, detail="Internal server error")
