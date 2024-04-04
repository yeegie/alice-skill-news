from fastapi import APIRouter, HTTPException, Response
from tortoise.exceptions import IntegrityError
from .dto import SessionCreateDto, SessionSchema, SessionAnswerDto
from database.models import User, Session
from datetime import datetime, timedelta

router = APIRouter()

@router.post('/', status_code=201, response_model=SessionSchema)
async def create(session_data: SessionCreateDto):
    try:
        user = await User.get_or_none(user_id=session_data.user_id)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        new_session = await Session.create(
            secret=session_data.secret,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=3),
            user=user
        )
        return new_session
    except IntegrityError as integrity_ex:
        raise HTTPException(status_code=409, detail="Record already exists")
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.get('/by/id/{id}')
async def get_all_by_id(id: int):
    try:
        return await Session.filter(user=id)
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.post('/answer')
async def answer(session_data: SessionAnswerDto):
    try:
        session = await Session.filter(active=True, secret=session_data.secret).get_or_none()
        if session is None: raise HTTPException(status_code=404, detail='Session not found.')

        user = await User.get(user_id=session.user_id)
        user.yandex_id = session_data.yandex_id
        await user.save()

        session.active = False
        await session.save()

        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.get('/active/{id}', status_code=200)
async def active(id: int):
    try:
        sessions = await Session.filter(active=True, user=id)
        if len(sessions) <= 0: raise HTTPException(status_code=404, detail='Sessions not found.')

        return sessions

    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.patch('/close_all/{id}', status_code=200)
async def close_all_sessions(id: int):
    try:
        user = await User.get_or_none(user_id=id)
        if user is None: raise HTTPException(status_code=404, detail='[Close all] User not found.')

        sessions = await Session.filter(active=True, user=id).update(active=False)
        if sessions is None: raise HTTPException(status_code=404, detail='[Close all] All sessions is unactive.')
        
        updated_sessions = await Session.filter(active=True)
        return updated_sessions
    
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
