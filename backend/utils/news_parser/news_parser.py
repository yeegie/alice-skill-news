from data.config import Pyrogram
from pyrogram import Client
from typing import List, Optional
from loguru import logger


class NewsParser:
    __api_id = Pyrogram.api_id
    __api_hash = Pyrogram.api_hash

    async def parse_channel(app: Client, channel_id: str) -> dict:
        result = {
            'channel_id': channel_id,
            'news': [],
            'detail': '',
        }

        # Magic ✨
        async for message in app.get_chat_history(channel_id, limit=100):
            # logger.info(f'{message.text}, TYPE: {type(message.text)}')
            if message.empty != True and message.text is not None:
                result['news'].append({
                    'text': message.text,
                    'date': message.date,
                    'views': message.views,
                    'link': message.link,
                })

        return result

    @classmethod
    async def run(cls, channels: List[str]):
        result = []

        async with Client('news_parser', cls.__api_id, cls.__api_hash) as app:
            logger.info('[🤖] News parser is working!')
            for i, channel in enumerate(channels):
                logger.info(f'[{i+1}/{len(channels)}] {channel} parse news...')
                news = await cls.parse_channel(app, channel)
                result.append(news)
        
        return result

