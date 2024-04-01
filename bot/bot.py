from data.config import Telegram, WebHook
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from aiogram.enums.parse_mode import ParseMode

from aiohttp.web import Application, run_app
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from middlewares.manage_users import ManageUserMiddleware
from handlers import routers


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    dispatcher.message.outer_middleware(ManageUserMiddleware())
    dispatcher.callback_query.outer_middleware(ManageUserMiddleware())
    logger.info(f"[2] Middlewares initialized...")

    dispatcher.include_router(router=routers.user_router)
    dispatcher.include_router(router=routers.admin_router)
    logger.info('[1] Routers included...')

    await bot.set_webhook(f"{WebHook.base_url}{WebHook.bot_path}")
    logger.info('[🌟] Bot started!')


async def on_shutdown():

    logger.info('===== Stopping the bot =====')
    await bot.delete_webhook()
    logger.info('[💀] WebHook - 👋!')
    logger.info('[💀] Bot - I\'ll be back.')

if __name__ == '__main__':
    props = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )

    bot = Bot(token=Telegram.token, default=props)
    storage = MemoryStorage()
    dispather = Dispatcher(storage=storage)
    dispather.startup.register(on_startup)
    dispather.shutdown.register(on_shutdown)

    app = Application()

    app['bot'] = bot
    app['dp'] = dispather

    SimpleRequestHandler(dispatcher=dispather, bot=bot).register(app, WebHook.bot_path)

    setup_application(app, dispather, bot=bot)
    run_app(app, host=WebHook.listen_address, port=WebHook.listen_port)
