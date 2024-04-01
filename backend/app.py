import database
from data.config import Backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from routes import user_router, session_router, channel_router, news_router  # device_router

from utils.session_updater import update_sessions

import uvicorn
from contextlib import asynccontextmanager

from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_sessions, 'interval', minutes=1)
    scheduler.start()

    logger.info('[⭐] Starting app...')
    await database.connect_database()
    yield
    logger.info('[👋] Bye')
    await database.desconnect_database()


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
