from fastapi import APIRouter, HTTPException, Response
from tortoise.exceptions import IntegrityError

from schemas.channel import ChannelSchema
from schemas.dto.channel import ChannelCreateDto

from models import Channel, User

from typing import List

from services.channel import ChannelService

from tortoise.exceptions import DoesNotExist


router = APIRouter()


@router.post('/', status_code=201)
async def create(channel_data: ChannelCreateDto):
    '''Create channel from dto'''
    await ChannelService.create(channel_data)


@router.get('/', response_model=List[ChannelSchema])
async def all():
    try:
        raise await ChannelService.all()
    except Exception as ex:
        raise HTTPException(500, str(ex))
    

@router.get('/{id}', response_model=ChannelSchema)
async def get(id: str):
    try:
        return await ChannelService.get(id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))


@router.post('/toggle/{id}', status_code=204)
async def toggle_visibility(id: str):
    '''Toggle visibility (active) in channel by uuid'''
    try:
        await ChannelService.toggle(id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
    

@router.delete('/{id}', status_code=204)
async def delete(id: str):
    '''Delete channel by uuid'''
    try:
        await ChannelService.delete(id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
