"""
Функции ​к​лиента:​
- сформировать ​​presence-сообщение;
- отправить ​с​ообщение ​с​ерверу;
- получить ​​ответ ​с​ервера;
- разобрать ​с​ообщение ​с​ервера;
- параметры ​к​омандной ​с​троки ​с​крипта ​c​lient.py ​​<addr> ​[​<port>]:
- addr ​-​ ​i​p-адрес ​с​ервера;
- port ​-​ ​t​cp-порт ​​на ​с​ервере, ​​по ​у​молчанию ​​7777.
"""
import sys
import logging
from socket import socket, AF_INET, SOCK_STREAM
from jim.config import *
from jim.utils import send_message, get_message

from jim.core import JimPresence, JimMessage, Jim, JimResponse



class User:

    def __init__(self, login):
        self.login = login

    def create_presence(self):
        """
        Сформировать ​​presence-сообщение
        :return: Словарь сообщения
        """
        # формируем сообщение
        jim_presence = JimPresence(self.login)
        message = jim_presence.to_dict()
        # возвращаем
        return message


    def translate_response(self, response):
        """
        Разбор сообщения
        :param response: Словарь ответа от сервера
        :return: корректный словарь ответа
        """
        result = Jim.from_dict(response)
        # возвращаем ответ
        return result.to_dict()


    def create_message(self, message_to, text):
        message = JimMessage(message_to, self.login, text)
        return message.to_dict()


    def read_messages(self, service):
        """
        Клиент читает входящие сообщения в бесконечном цикле
        :param client: сокет клиента
        """
        while True:
            # читаем сообщение
            print('Читаю')
            message = get_message(service)
            print(message)
            # там должно быть сообщение всем
            print(message[MESSAGE])


    def write_messages(self, service):
        """Клиент пишет сообщение в бесконечном цикле"""
        while True:
            # Вводим сообщение с клавиатуры
            text = input(':)>')
            # Создаем jim сообщение
            message = self.create_message('#all', text)
            # отправляем на сервер
            send_message(service, message)


if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    # Пытаемся получить параметры скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    try:
        mode = sys.argv[3]
    except IndexError:
        mode = 'r'
    # Соединиться с сервером
    sock.connect((addr, port))
    # Создаем пользователя
    user = User('Leo')
    # Создаем сообщение
    presence = user.create_presence()
    # Отсылаем сообщение
    send_message(sock, presence)
    # Получаем ответ
    response = get_message(sock)
    # Проверяем ответ
    response = user.translate_response(response)
    if response['response'] == OK:
        # в зависимости от режима мы будем или слушать или отправлять сообщения
        if mode == 'r':
            user.read_messages(sock)
        elif mode == 'w':
            user.write_messages(sock)
        else:
            raise Exception('Не верный режим чтения/записи')
