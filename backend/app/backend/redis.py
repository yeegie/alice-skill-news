from redis.asyncio import Redis
from .config import Redis as RedisConfig

from loguru import logger


client = Redis(host=RedisConfig.host, port=RedisConfig.port)
