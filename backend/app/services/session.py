from models import Session
from datetime import datetime
from loguru import logger


class SessionService():
    @staticmethod
    async def checker():
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
