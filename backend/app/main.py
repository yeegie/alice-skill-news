from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import uvicorn
from contextlib import asynccontextmanager

from backend.database import connect_database, desconnect_database
from backend.config import Backend

from services.session import SessionService

from routers import *

from loguru import logger


LOG_OUT_FILE = 'logs/backend.log'
logger.add(LOG_OUT_FILE, rotation='10 MB', compression='zip', level='DEBUG')


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(SessionService.checker, 'interval', minutes=1)
    scheduler.start()

    logger.info('[⭐] Starting app...')
    await connect_database()
    yield
    logger.info('[👋] Bye')
    await desconnect_database()


app = FastAPI(title='alice news skill', debug=True, lifespan=lifespan)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

# Routes
app.include_router(user_router, prefix='/users', tags=['users'])
app.include_router(session_router, prefix='/sessions', tags=['sessions'])
app.include_router(channel_router, prefix='/channels', tags=['channels'])
app.include_router(news_router, prefix='/news', tags=['news'])

if __name__ == '__main__':
    uvicorn.run(app, host=Backend.host, port=Backend.port)
