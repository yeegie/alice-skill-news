from fastapi import APIRouter, status, HTTPException
from .dto import DeviceCreateDto, DeviceUpdateDto, DeviceSchema
from typing import List

from database.models import Device, User

router = APIRouter()


@router.post('/', status_code=201, response_model=DeviceSchema)
async def create(device_data: DeviceCreateDto):
    try:
        user = await User.get_or_none(user_id=device_data.user_id)
        if user is None: raise HTTPException(status_code=404, detail='User not found!')
        new_device = await Device.create(
            title=device_data.title,
            user=user
        )
        return new_device
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get('/', response_model=List[DeviceSchema])
async def all():
    try:
        return await Device.all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
