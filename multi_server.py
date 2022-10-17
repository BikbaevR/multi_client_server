import socket
import threading
from pathlib import Path
from datetime import datetime
import time

IP = '192.168.236.25'
PORT = 8803
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!dis"
OPEN_MSG = "!open"
WRITE_MSG = "!w"

dir_path = Path(r"\\Rafael\лаба 2")
file_name = 'main.txt'
create = 'null'
global conn
locker = threading.Lock()

global t
global h

try:
    file = open(dir_path.joinpath(file_name))
    print('\033[32m[СЕРВЕР] Файл найден!\033[0m')
except:
    print('[СЕРВЕР] Файл не найден!')
    create = input('[СЕРВЕР] Создать файл y/n?')

if create == 'y':
    if dir_path.is_dir():
        with open(dir_path.joinpath(file_name), 'a+') as f:
            f.write("This text is written in python\n")
        print('[СЕРВЕР] Файл создан')
    else:
        print('[СЕРВЕР] Каталог не существует')
if create == 'n':
    print('[СЕРВЕР] Вы выбрали не создавать файл')


def timer(sec):
    timing = time.time()
    while True:
        if time.time() - timing > sec:
            timing = time.time()
            return True


def handle_client(conn, addr):
    ZAPIS = False
    print(f"\033[43m[НОВОЕ ПОДКЛЮЧЕНИЕ] {addr} подключен\033[0m")

    connected = True
    while connected:

        # current_datetime = datetime.now().time()
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False


            print(f"[КЛИЕНТ] [{addr}] {msg}")
            msg = f"[СЕРВЕР] Вы отключены от сервера"
            conn.send(msg.encode(FORMAT))

        if msg == OPEN_MSG:
            print(f"[СЕРВЕР] {threading.get_ident()} Получен запрос на запись в файл")
            ZAPIS = True
            msg = f'[СЕРВЕР] {threading.get_ident()} Запись в файл начата'
            conn.send(msg.encode(FORMAT))
            change()

        if msg == WRITE_MSG:
            change()
        # conn.close()





def change():


    locker.acquire()
    file = open(dir_path.joinpath(file_name), 'a+')
    file.write(f"[СЕРВЕР] Файл открыт клиентом '{threading.get_ident()}' в {datetime.now().time()}\n")
    file.write(f"[КЛИЕНТ '{threading.get_ident()}'] Запись в файл\n")
    timer(5)
    file.write(f"[СЕРВЕР] Файл закрыт клиентом '{threading.get_ident()}' в {datetime.now().time()}\n\n")
    file.close()
    print(f"\033[32m[СЕРВЕР] Клиент '{threading.get_ident()}' произвел запись в файл\033[0m")
    ZAPIS = False
    locker.release()


def main():
    global conn
    global thread
    print("\033[31m[ЗАПУСК] Сервер запущен...\033[0m")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"\033[31m[ПРОСЛУШИВАНИЕ] Сервер в режиме прослушивания {IP}:{PORT}\033[0m")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\033[43m[АКТИВНЫЕ СОЕДИНЕНИЯ] {threading.active_count() - 1}\033[0m")


if __name__ == "__main__":
    main()
