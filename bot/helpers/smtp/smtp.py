import aiosmtplib
import uuid

from email.message import EmailMessage

from loguru import logger


class SMTPService:
    _smtp_params = {}

    def __init__(self, host, port, user, password):
        self._smtp_params['TLS'] = True
        self._smtp_params['host'] = host
        self._smtp_params['port'] = port
        self._smtp_params['user'] = user
        self._smtp_params['password'] = password

    async def connect(self):
        self.smtp = aiosmtplib.SMTP(
            hostname=self._smtp_params['host'],
            port=self._smtp_params['port'],
            start_tls=False,
            use_tls=False,
        )
        await self.smtp.connect()
        await self.smtp.starttls()

    async def login(self):
        await self.smtp.login(self._smtp_params['user'], self._smtp_params['password'])

    async def kill(self):
        await self.smtp.quit()

    async def send_confirm_code(self, to):
        secret = str(uuid.uuid4()).split('-')[0]

        message = EmailMessage()
        message['From'] = self._smtp_params['user']
        message['To'] = to
        message['Subject'] = 'Код подтверждения'
        message.set_content(f'Ваш код: {secret}')

        await self.smtp.send_message(message, recipients=to)

        return (secret)
