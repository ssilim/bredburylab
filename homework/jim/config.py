"""Константы для jim протокола, настройки"""
# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'

# Значения
PRESENCE = 'presence'
MSG = 'msg'
TO = 'to'
MESSAGE = 'message'
FROM = 'from'


# Коды ответов (будут дополняться)
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500

# Кортеж из кодов ответов
RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)

USERNAME_MAX_LENGTH = 25
MESSAGE_MAX_LENGTH = 500

ACTIONS = (PRESENCE, MSG)
