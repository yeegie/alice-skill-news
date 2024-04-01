from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')


class Backend:
    section = 'Backend'
    host = parser.get(section, 'host')
    port = parser.getint(section, 'port')


class MySQL:
    section = 'MySQL'
    host = parser.get(section, 'host')
    port = parser.getint(section, 'port')
    user = parser.get(section, 'user')
    password = parser.get(section, 'password')
    database = parser.get(section, 'database')

    connection_string = f'mysql://{user}:{password}@{host}:{port}/{database}'


class Pyrogram:
    section = 'Pyrogram'
    api_id = parser.get(section, 'api_id')
    api_hash = parser.get(section, 'api_hash')
