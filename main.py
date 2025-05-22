from contextlib import asynccontextmanager
import logging.config

import uvicorn
import yaml
from fastapi import FastAPI

from app.core.config import settings
from app.api.user import router as users_router
from app.db.db_manager import db_manager
from app.db.initial_data import initialize_users

with open(settings.log.config_path, "r", encoding=settings.log.encoding) as file:
    config = yaml.safe_load(file.read())

logging.config.dictConfig(
    config=config
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.create_tables()
    
    # init 1000 users, if DB is empty
    await initialize_users(session_gen=db_manager.session_getter())
    yield
    await db_manager.engine_dispose()
    

app = FastAPI(
    lifespan=lifespan
)

app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.api.host,
        port=settings.api.port,
    )