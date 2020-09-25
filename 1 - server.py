''' Создает блокирующие вызовы
в один момент подлкючен только 1 клиент'''

import socket

# address domain:5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Повторное использование порта в случае отключения
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Привязка к адресу и прослушка подключений
server_socket.bind(('localhost', 5000))
server_socket.listen()


# Бесконечная прокрутка
while True:
    print ('Before .accept()')
    client_socket, addr = server_socket.accept() # кортеж из двух переменных
    print('Connection from', addr)

    while True:
        print('Before .receive()')
        request = client_socket.recv(4096) # принятие пакета размером 4кб

        if not request:
            break

        else:
            response = 'Hello world\n'.encode()
            client_socket.send(response)

    print('Outside')
    client_socket.close()