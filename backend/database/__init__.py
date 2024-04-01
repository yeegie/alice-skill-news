from tortoise import Tortoise
from data.config import MySQL
from loguru import logger

modules = {'models': ['database.models']}


async def connect_database(*_, **__):
    await Tortoise.init(db_url=MySQL.connection_string, modules=modules)
    await Tortoise.generate_schemas()
    logger.info('[📦] Database connected.')


async def desconnect_database():
    await Tortoise.close_connections()
    logger.info('[X] Database connection close!')
