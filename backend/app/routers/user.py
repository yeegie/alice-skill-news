from fastapi import APIRouter, HTTPException, Response

from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto

from models import User, News
from tortoise.exceptions import IntegrityError, DoesNotExist, ValidationError

from services.user import UserService

from typing import List

router = APIRouter()

from loguru import logger

prefetch_list = ['sessions', 'channels', 'news']


@router.post('/', status_code=201)
async def create(user_data: UserCreateDto):
    try:
        await UserService.create(user_data)
    except Exception as ex:
        logger.error(str(ex))


@router.put('/{id}')
async def update(id: str, user_data: UserUpdateDto):
    try:
        user = await UserService.update(id, user_data)
        return user
    except ValidationError as ex:
        logger.error(f'[429] {str(ex)}')
        return HTTPException(429, detail=str(ex))
    except Exception as ex:
        logger.error(f'[500] {str(ex)}')
        return HTTPException(500, detail=str(ex))


@router.get('/')
async def get_all():
    try:
        users = await UserService.get_all()
        return users
    except Exception as ex:
        logger.error(f'[500] {str(ex)}')
        return HTTPException(500, detail=str(ex))


@router.get('/{id}')
async def get(id: str):
    '''Get user by pk'''
    try:
        user = await UserService.get(id)
        return user
    except DoesNotExist as ex:
        return HTTPException(404, detail=str(ex))
    except Exception as ex:
        logger.error(f'[500] {str(ex)}')
        return HTTPException(500, detail=str(ex))


@router.get('/by-user_id/{user_id}')
async def get_by_user_id(user_id: int):
    '''Get user by unique Telegram ID'''
    try:
        user = await UserService.get_by_user_id(user_id)
        return user
    except HTTPException as ex:
        return HTTPException(404, detail=str(ex))
    except Exception as ex:
        return HTTPException(500, detail=str(ex))


@router.get('/by-yandex_id/{yandex_id}')
async def get_by_yandex_id(yandex_id: str):
    '''Get user by unique Yandex ID'''
    try:
        user = await UserService.get_by_yandex_id(yandex_id)
        return user
    except HTTPException as ex:
        return HTTPException(404, detail=str(ex))
    except Exception as ex:
        return HTTPException(500, detail=str(ex))


@router.delete('/{id}', status_code=204)
async def delete(id: str):
    '''Delete user by UUID (pk)'''
    try:
        await UserService.delete(id)
    except HTTPException as ex:
        return HTTPException(404, detail=str(ex))
    except Exception as ex:
        return HTTPException(500, detail=str(ex))
