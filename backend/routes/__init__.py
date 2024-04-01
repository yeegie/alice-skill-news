from .users import router as user_router
from .channels import router as channel_router
from .sessions import router as session_router
from .news import router as news_router

# под вопросом
# from .devices import router as device_router


__all__ = [
    'user_router',
    'channel_router',
    'news_router',
    'session_router',
]
