from database.models import Session
from datetime import datetime, timezone
from loguru import logger


async def update_sessions():
    sessions = await Session.filter(active=True)
    
    sessions_closed = 0
    for session in sessions:
        # Убираем смещение времени
        time_end = session.end_time.replace(tzinfo=None)
        time_now = datetime.now().replace(tzinfo=None)

        if time_end <= time_now:
            session.active = False
            await session.save()
            sessions_closed += 1

    if sessions_closed != 0:
        logger.info(f'[i] Сессий закрыто: {sessions_closed}')
