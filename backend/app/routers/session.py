from fastapi import APIRouter, HTTPException, Response
from tortoise.exceptions import IntegrityError, DoesNotExist

from schemas.session import SessionSchema
from schemas.dto.session import SessionCreateDto, SessionAnswerDto

from models import User, Session
from datetime import datetime, timedelta

from services.session import SessionService


router = APIRouter()


@router.post('/', status_code=201, response_model=SessionSchema)
async def create(session_data: SessionCreateDto, lifetime: int = 3):
    '''
    Create session from body\n
    params:
    * lifetime -- session lifetime in minutes, default=3
    '''
    try:
        return await SessionService.create(session_data, lifetime)
    except IntegrityError as ex:
        raise HTTPException(409, str(ex))
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
    

@router.get('/avaiable/{user_id}', response_model=SessionSchema)
async def get_all_by_id(user_id: int):
    '''Get active user sessions by Telegram ID'''
    try:
        return await SessionService.avaiable(user_id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))

    

@router.post('/answer', status_code=204)
async def answer(secret: str, yandex_id: str):
    '''
    Search active session by secret and then close it, write to user yandex_id\n
    params:
    * secret -- secret word in session
    * yandex_id -- unique id in yandex services
    '''
    try:
        await SessionService.answer(secret, yandex_id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
    

@router.get('/active/{user_id}', status_code=200)
async def active(user_id: int):
    try:
        sessions = await SessionService.active(user_id)
        return sessions
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
    

@router.patch('/close_all/{user_id}', status_code=204)
async def close_all_sessions(user_id: int):
    '''
    Close all active user sessions\n
    params:
    * user_id -- telegram user id
    '''
    try:
        await SessionService.close_all(user_id)
    except DoesNotExist as ex:
        raise HTTPException(404, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
