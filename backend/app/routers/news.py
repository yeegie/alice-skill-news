from fastapi import APIRouter, HTTPException, Response

from schemas.news import NewsSchema
from schemas.dto.news import NewsCreateDto, NewsUpdateDto

# from utils import NewsParser
from models import User, Channel

from loguru import logger


router = APIRouter()


@router.post('/', status_code=201)
async def create(news_data: NewsCreateDto):
    try:
        pass
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.get('/get/{user_id}')
async def get_news(user_id: int):
    '''user_id: is telegram user id'''
    try:
        channels = await Channel.filter(user=user_id, active=True)
        if channels is None: raise HTTPException(status_code=404, detail='Channels list is empty')

        channels_list = []
        for channel in channels:
            channels_list.append(channel.channel_id)

        # news = await NewsParser.run(channels_list)
        # return news
    except HTTPException as http_ex:
        return Response(status_code=http_ex.status_code, content=http_ex.detail)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))