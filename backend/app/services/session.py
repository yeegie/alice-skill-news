from models import Session, User
from schemas.session import SessionSchema
from schemas.dto.session import SessionCreateDto, SessionUpdateDto, SessionAnswerDto
from datetime import datetime, timedelta
from loguru import logger
from tortoise.exceptions import DoesNotExist, IntegrityError

from typing import List

from .user import UserService

from .notification import NotificationService
from schemas.notification import NotificationSchema


class SessionService():
    @staticmethod
    async def create(dto: SessionCreateDto, lifetime: int = 3) -> SessionSchema:
        '''Create session from dto'''
        try:
            await UserService.get_by_user_id(dto.user_id)
        except DoesNotExist as ex:
            raise DoesNotExist(str(ex))

        try:
            session = await Session.create(
            user_id=dto.user_id,
            secret=dto.secret,
            end_time=datetime.now() + timedelta(minutes=lifetime),
            )
        except IntegrityError as ex:
            raise IntegrityError('Secret word is not unique')
        
        logger.info(f'[{session.id}] New session!')
        return await session.to_schema()
    

    @staticmethod
    async def avaiable(user_id: int) -> SessionSchema:
        '''Get active user sessions by Telegram ID'''
        session = await Session.get_or_none(user_id=user_id)
        if session is None: raise DoesNotExist('Session not found')
        return await session.to_schema()
    

    @staticmethod
    async def answer(secret: str, yandex_id: str) -> None:
        '''
        Search active session by secret and then close it, write to user yandex_id\n
        params:
        * secret -- secret word in session
        * yandex_id -- unique id in yandex services
        '''
        session = await Session.get_or_none(secret=secret)
        if session is None: raise DoesNotExist('Sesson not found')
        
        # ! Плохое решение, потом заменить !
        user = await User.get_or_none(user_id=session.user_id)
        if user is None: raise DoesNotExist('User not found')
        
        user.yandex_id = yandex_id
        session.active = False

        await user.save()
        await session.save()

        await NotificationService.send(NotificationSchema(
            target=user.user_id,
            message='Профиль обновлен, учетные записи связаны 🔗',
        ))

    
    @staticmethod
    async def active(user_id: int) -> List[SessionSchema]:
        sessions = await Session.filter(active=True, user=user_id)
        if len(sessions) <= 0: raise DoesNotExist('Active sessions not found')
        return [await session.to_schema() for session in sessions]


    @staticmethod
    async def close_all(user_id: int):
        '''
        Close all active user sessions\n
        params:
        * user_id -- telegram user id
        '''
        try:
            user = await UserService.get_by_user_id(user_id)
        except DoesNotExist as ex:
            raise DoesNotExist(str(ex))
        
        sessions = await Session.filter(active=True, user_id=user.user_id).update(active=False)
        if sessions is None:
            raise DoesNotExist('All sessions unactive')



    @staticmethod
    async def checker():
        '''Sets active=False for sessions whose time has expired'''
        sessions = await Session.filter(active=True)

        session_closed = 0
        for session in sessions:
            # Убираем смещение времени
            time_end = session.end_time.replace(tzinfo=None)
            time_now = datetime.now().replace(tzinfo=None)

            if time_end <= time_now:
                session.active = False
                await session.save()
                session_closed += 1
        
        if session_closed != 0:
            logger.info(f'[i] Sessions killed: {session_closed}')
