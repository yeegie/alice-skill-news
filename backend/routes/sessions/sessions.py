from fastapi import APIRouter, HTTPException, Response
from tortoise.exceptions import IntegrityError
from .dto import SessionCreateDto, SessionSchema, SessionAnswerDto
from database.models import User, Session
from datetime import datetime, timedelta
from utils.word_generator import WordGenerator

router = APIRouter()

@router.post('/', status_code=201, response_model=SessionSchema)
async def create(session_data: SessionCreateDto):
    try:
        user = await User.get_or_none(user_id=session_data.user_id)
        if user is None: raise HTTPException(status_code=404, detail='User not found.')
        new_session = await Session.create(
            secret=WordGenerator.generate(),
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
    

@router.post('/answer')
async def answer(session_data: SessionAnswerDto):
    try:
        session = await Session.filter(active=True, secret=session_data.secret).get_or_none()
        if session is None: raise HTTPException(status_code=404, detail='Session not found.')

        user = await User.get(user_id=session.user_id)
        user.yandex_id = session_data.yandex_id
        await user.save()
        return user
    except HTTPException as http_ex:
        return Response(content=http_ex.detail, status_code=http_ex.status_code)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))