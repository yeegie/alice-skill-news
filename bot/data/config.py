import configparser

parser = configparser.ConfigParser()
parser.read(r'config.ini')


def set_value(section, key, value):
    parser.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)


class Telegram:
    section = 'Telegram'
    token = parser.get(section, 'token')


class API:
    section = 'API'
    base_url = parser.get(section, 'base_url')


class WebHook:
    section = 'WebHook'
    listen_address = parser.get(section, 'listen_address')
    listen_port = parser.getint(section, 'listen_port')
    base_url = parser.get(section, 'base_url')
    bot_path = parser.get(section, 'bot_path')


class SMTP:
    section = 'SMTP'
    host = parser.get(section, 'host')
    port = parser.getint(section, 'port')
    user = parser.get(section, 'user')
    password = parser.get(section, 'password')
