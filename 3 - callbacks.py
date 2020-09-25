'''Асинхронность на колбэках'''

import socket
import selectors

# Default selector
selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    # Регистрируем файловый объект - серверный сокет
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
    # Регистрируем файловый объект - клиентский сокет
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096) # принятие пакета размером 4кб

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        # Снимем с регистрации перед закрытием
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = selector.select() # список именованных кортежей вида (key, events)
        # SelectorKey - именованный кортеж - (fileobj, events, data)

        for key, _ in events:
            callback = key.data    # это переданные колбэки
            callback(key.fileobj)   # это сами сокеты - аргументы в колбэки

if __name__ == '__main__':
    server()
    event_loop()