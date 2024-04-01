from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError
from .dto import ChannelCreateDto, ChannelSchema
from database.models import Channel, User
from typing import List


router = APIRouter()


@router.post('/', status_code=201, response_model=ChannelSchema)
async def create(channel_data: ChannelCreateDto):
    try:
        user = await User.get_or_none(user_id=channel_data.user_id)
        if user is None: raise HTTPException(status_code=404, detail='User not found')
        new_channel = await Channel.create(
            title=channel_data.title,
            channel_id=channel_data.channel_id,
            user=user
        )
        return new_channel
    except IntegrityError as integrity_ex:
        raise HTTPException(status_code=409, detail='Record already exists')
    except HTTPException as http_ex:
        raise HTTPException(status_code=http_ex.status_code, detail=http_ex.detail)
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))


@router.get('/', response_model=List[ChannelSchema])
async def all():
    try:
        return await Channel.all()
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))
