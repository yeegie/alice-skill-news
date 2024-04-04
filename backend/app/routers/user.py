from fastapi import APIRouter, HTTPException, Response

from schemas.user import UserSchema
from schemas.dto.user import UserCreateDto, UserUpdateDto

from models import User, News
from tortoise.exceptions import IntegrityError, DoesNotExist

from services.user import UserService

from typing import List

router = APIRouter()

from loguru import logger

prefetch_list = ['sessions', 'channels', 'news']


@router.post('/', status_code=201)
async def create(user_data: UserCreateDto):
    # try:
    #     user = await User.create(
    #         user_id=user_data.user_id,
    #         email=user_data.email,
    #         full_name=user_data.full_name,
    #         username=user_data.username,
    #     )
    #     news = await News.create(
    #         user=user
    #     )
    #     return user
    # except IntegrityError as integrity_ex:
    #     raise HTTPException(status_code=409, detail="Record already exists")
    # except Exception as ex:
    #     raise HTTPException(status_code=500, detail=str(ex))
    try:
        await UserService.create(user_data)
    except Exception as ex:
        logger.error(str(ex))


@router.put('/{id}')
async def update(id: str, user_data: UserUpdateDto):
    try:
        user = await User.get_or_none(id=id).prefetch_related(*prefetch_list)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        await user.update_from_dict(user_data.model_dump())
        await user.save()
        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get('/check/{id}')
async def check(id: str):
    try:
        user = await User.get_or_none(id=id).prefetch_related(*prefetch_list)
        if user is None:
            return { 'is_exist': False }
        else:
            return { 'is_exist': True, 'user': user }
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get('/by/id/{id}')
async def find_one_by_id(id: str):
    try:
        user = await UserService.get_user(id)
    except DoesNotExist as ex:
        return Response(ex, 404)
    except Exception as ex:
        logger.error(f'[500] {str(ex)}')
        return Response('Ops..', 500)

    

@router.get('/by/email/{email}', response_model=UserSchema)
async def find_one_by_email(email: str):
    try:
        user = await User.get_or_none(email=email).prefetch_related(*prefetch_list)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get('/by/user_id/{id}', response_model=UserSchema)
async def find_one_by_user_id(id: int):
    try:
        user = await User.get_or_none(user_id=id).prefetch_related(*prefetch_list)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.get('/by/yandex_id/{id}', response_model=UserSchema)
async def find_one_by_yandex_id(id: str):
    try:
        user = await User.get_or_none(yandex_id=id).prefetch_related(*prefetch_list)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get('/', response_model=List[UserSchema])
async def find_all():
    users = await User.all().prefetch_related(*prefetch_list)

    return users


@router.delete('/{id}', status_code=204)
async def delete(id: str):
    try:
        user = await User.get_or_none(id=id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found.')
        await user.delete()
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=str(ex))
