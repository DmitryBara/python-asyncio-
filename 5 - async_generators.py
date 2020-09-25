import socket
from select import select

# Непосредственно задачи
# Лучше реализовать очередями
tasks = []

# Сырье для списка tasks
to_read = {} # { socket: generator }
to_write = {} # { socket: generator }

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:

        yield ('read', server_socket) # елдим кортеж с меткой
        client_socket, addr = server_socket.accept() # read

        print('Connection from', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        # первый параметр нужен для роутинга сокетов в словари
        yield ('read', client_socket)
        request = client_socket.recv(4096)  # read

        if not request:
            break
        else:
            response = 'Hello world\n'.encode() # write

            yield ('write', client_socket)
            client_socket.send(response)


    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):

        # Обеспечиваем список tasks новыми элементами
        while not tasks:
            # создаем словари из сокетов, готовых для read/write
            ready_to_read, ready_to_write, errors = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task

        except StopIteration:
            print("Disconnect!")

tasks.append(server())
event_loop()

