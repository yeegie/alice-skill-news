# Навык "Новости" для станций Яндекс

![Network Diagram](https://github.com/yeegie/alice-skill-news/docs/NetworkDiagram.png)

# Установка

0. Создайте виртуальное окружение и активируйте его
``` shell
python -m venv venv
```
Для Windows
``` shell
source .\venv\Scripts\activate
```
Для Linux
``` shell
source ./venv/bin/activate
```

1. Установите зависимости в ваше виртуальное окружение
``` shell
pip install -r requirements.txt
```

2. Перейдите на платформу [Яндекс Диалоги](https://dialogs.yandex.ru/developer) и создайте диалог:
	* В поле __backend__ выберите Webhook URL и впишите адрес back-end приложения на который будут поступать запросы.
	* В поле тип доступа обязательно выбираем __приватный__, чтобы не проходить модерацию, тем не менее навык будет доступен на вашем аккаунте.
	* Сохраняем навык, ждем пока он станет доступен. 

3. Запустите бэкенд, бота и приложение для обработки запросов (по сути логику навыка)
``` shell
python .\backend\app.py
python .\bot\bot.py
python .\alice\app.py
```
   

# Использование
1. Зайдите в телеграм бота, токен которого вы указали в bot/config, пройдите регистрацию.
2. Начните процесс связывания аккаунта, вам будет сообщена секретная фраза.
3. Начните диалог с Алисой и снова начните процесс связывания, сообщите секретную фразу.
4. В телеграм боте добавьте интересующие вас каналы.
5. Чтобы узнать о новых постах в каналах, спросите Алису -- что нового?

# Файлы конфигурации
Ниже будут небольшие комментарии и выделенные поля, которые нужно заполнить.
### backend/config.ini
[Backend]  На каком хосте и порте будет развёрнуто приложение
1. host = localhost
2. port = 8000

[MySQL] Данные от базы данных MySQL
1. host = localhost
2. port = 3306
3. user = user
4. <u>password = password
5. database = alice_news

[TelegramAPI] Регистрируем приложение [тут](https://my.telegram.org/auth?to=apps), вводим данные ниже
1. api_id=12345678
2. api_hash=27super218892secret3949token231

<hr>

### bot/config.ini
[Telegram] Токен бота из [Bot Father](https://t.me/BotFather)
1. token=123123:SIDsdiosadiS12

[API]
1. base_url=http://localhost:8000/

[WebHook] 
1. listen_address = localhost
2. listen_port = 5000
3. base_url = https://63e6-94-241-173-114.ngrok-free.app
4. bot_path = /bot

[SMTP] Данные от аккаунта гугл, для отправки писем с кодом подтвержения
1. host=smtp.gmail.com
2. port=587
3. user=mail.noreply@gmail.com
4. password=111 2341 2312


# Полезная информация
* Для отладки Алисы локально советую использовать [alice-nearby](https://github.com/azzzak/alice-nearby).
* Для отладки бота можете использовать [port forwarding](https://code.visualstudio.com/docs/editor/port-forwarding) в VS Code или [ngrok](https://ngrok.com/).
