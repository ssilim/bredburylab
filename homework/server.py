"""
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
"""
import sys
import json
import select
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import dict_to_bytes, bytes_to_dict, send_message, get_message
from jim.config import *


def presence_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return: Словарь ответа
    """
    # Делаем проверки
    if ACTION in presence_message and \
                    presence_message[ACTION] == PRESENCE and \
                    TIME in presence_message and \
            isinstance(presence_message[TIME], float):
        # Если всё хорошо шлем ОК
        return {RESPONSE: 200}
    else:
        # Шлем код ошибки
        return {RESPONSE: 400, ERROR: 'Не верный запрос'}


class Handler:
    def read_requests(self, r_clients, all_clients):

        messages = []

        for sock in r_clients:
            try:
                message = get_message(sock)
                #
                messages.append(message)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)

        return messages

    def write_responses(self, messages, w_clients, all_clients):
        for sock in w_clients:
            for message in messages:
                try:
                    send_message(sock, message)
                except:
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)



class Server:
    def __init__(self, handler):
        self.handler = handler
        self.clients = []
        self.sock_server = socket(AF_INET, SOCK_STREAM)

    def bind(self, addr, port):
        self.sock_server.bind((addr, port))

    def listen_forever(self):
        self.sock_server.listen(15)
        self.sock_server.settimeout(0.2)


        while True:
            try:
                conn, addr = self.sock_server.accept()  # Принять запрос на соединение
                presence = get_message(conn)
                print('<presence>:', presence)
                responce = presence_response(presence)
                send_message(conn, responce)
            except OSError as e:
                pass
            else:
                print('Получен запрос на соеденение: %s' % str(addr))
                self.clients.append(conn)
                print('<client_list>:', self.clients)
            finally:
                # Проверить наличие событий ввода-вывода
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = self.handler.read_requests(r, self.clients)  # Получаем входные сообщения
                self.handler.write_responses(requests, w, self.clients)  # Выполним отправку входящих сообщений



if __name__ == '__main__':
    # server = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    # Получаем аргументы скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    handler = Handler()
    server = Server(handler)
    server.bind(addr, port)
    server.listen_forever()