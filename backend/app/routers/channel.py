from fastapi import APIRouter, HTTPException, Response
from tortoise.exceptions import IntegrityError

from schemas.channel import ChannelSchema
from schemas.dto.channel import ChannelCreateDto

from models import Channel, User

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
    

@router.get('/by/id/{id}', response_model=ChannelSchema)
async def find_one_by_id(id: str):
    try:
        channel = await Channel.get_or_none(id=id)
        if channel is None: raise HTTPException(status_code=404, detail='Channel not found.')
        return channel
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post('/toggle/{id}', response_model=ChannelSchema)
async def toggle_visibility(id: str):
    try:
        channel = await Channel.get_or_none(id=id)
        if channel is None: raise HTTPException(status_code=404, detail='Channel not found.')
        channel.active = not channel.active
        await channel.save()
        return channel
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.delete('/{id}', status_code=204)
async def delete(id: str):
    try:
        channel = await Channel.get_or_none(id=id)
        if channel is None:
            raise HTTPException(status_code=404, detail='Сhannel not found.')
        await channel.delete()
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=str(ex))
