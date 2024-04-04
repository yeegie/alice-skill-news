from data.config import Telegram, WebHook, SMTP
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from aiogram.enums.parse_mode import ParseMode

from aiohttp.web import Application, run_app
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from middlewares.manage_users import ManageUserMiddleware
from handlers import routers

from helpers.smtp import SMTPService
from models.smtp.params import SmtpParams

import time


LOG_OUT_FILE = 'logs/bot.log'
logger.add(LOG_OUT_FILE, rotation='10 MB', compression='zip', level='DEBUG')


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info(f'[⏳] Starting to launch the application...')
    time_start = time.time()

    await smtp_service.connect()
    logger.info('[3] SMTP service runned...')

    dispatcher.message.outer_middleware(ManageUserMiddleware())
    dispatcher.callback_query.outer_middleware(ManageUserMiddleware())
    logger.info(f"[2] Middlewares initialized...")

    dispatcher.include_router(router=routers.user_router)
    dispatcher.include_router(router=routers.admin_router)
    logger.info('[1] Routers included...')

    await bot.set_webhook(f"{WebHook.base_url}{WebHook.bot_path}")
    logger.info(f'[🌟] Bot started -- {(time.time() - time_start):.1f} sec.')


async def on_shutdown():
    logger.info('===== Stopping the bot =====')
    await bot.delete_webhook()
    logger.info('[💀] WebHook - 👋!')
    await smtp_service.kill()
    logger.info('[💀] SMTP service killed.')

    logger.info('[💀] Bot - I\'ll be back.')

if __name__ == '__main__':
    # SMTP
    _smtp_params = SmtpParams(
        tls=True,
        host=SMTP.host,
        port=SMTP.port,
        user=SMTP.user,
        password=SMTP.password,
    )
    smtp_service = SMTPService(params=_smtp_params)

    # Bot
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
