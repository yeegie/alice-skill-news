from aiosmtplib import SMTP
from aiosmtplib.errors import SMTPConnectTimeoutError

import uuid

from models.smtp.params import SmtpParams

from email.message import EmailMessage

from typing import Optional

from loguru import logger
import time


class Singleton(type):
    '''
    Метакласс Singleton для создания единственного экземпляра класса SMTPService
    '''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SMTPService(metaclass=Singleton):
    """
    Сервис для работы с SMTP-сервером для отправки электронной почты.
    """
    _smtp_params: SmtpParams
    _smtp: SMTP
    is_connected: bool

    def __init__(self, params: Optional[SmtpParams] = None) -> None:
        """
        Инициализирует объект сервиса SMTP с указанными параметрами.
        """
        self._smtp_params = params

        self._smtp = SMTP(
            hostname=params.host,
            port=params.port,
        )

        self.is_connected = self._smtp.is_connected


    async def connect(self):
        """
        Подключается к SMTP-серверу и выполняет вход.
        """
        try:            
            await self._smtp.connect()
            await self._smtp.login(
                self._smtp_params.user,
                self._smtp_params.password
                )
            self.is_connected = self._smtp.is_connected
        except SMTPConnectTimeoutError as timeout_ex:
            logger.error(f'[🚨] {timeout_ex}')
            logger.info(f'[i] Trying connect again afrer 10 sec delay... SMTP service now NOT WORKING')
            time.sleep(10)
            logger.info(f'[⟳] Lets retry connect!')
            await self.connect()
        except Exception as ex:
            logger.error(ex)
        finally:
            self.is_connected = self._smtp.is_connected


    async def kill(self):
        """
        Завершает соединение с SMTP-сервером.
        """
        await self._smtp.quit()
        self.is_connected = self._smtp.is_connected

    async def send_confirm_code(self, to):
        '''
        Отправляет письмо на указанный адрес с секретным кодом, возвращает секретный код.
        '''
        secret = str(uuid.uuid4()).split('-')[0]

        message = EmailMessage()
        message['From'] = self._smtp_params.user
        message['To'] = to
        message['Subject'] = 'Код подтверждения'
        message.set_content(f'Ваш код: {secret}')

        try:
            await self._smtp.send_message(message, recipients=to)
        except Exception as ex:
            logger.error(f'[!] {str(ex)}')

        return (secret)
