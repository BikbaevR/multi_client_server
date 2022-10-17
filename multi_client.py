import socket
from pathlib import Path
from datetime import datetime
import threading
import time

dir_path = Path(r"\\Rafael\лаба 2")
file_name = 'main.txt'

IP = '127.0.0.1'
PORT = 8803
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!dis"
OPEN_MSG = "!open"
WRITE_MSG = "!w"

def timer(sec):
    timing = time.time()
    while True:
        if time.time() - timing > sec:
            timing = time.time()
            return True


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[ПОДКЛЮЧЕНИЕ] Клиент подключен к серверу {IP}:{PORT}")

    connected = True
    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        if msg == WRITE_MSG:
            client.send(msg.encode(FORMAT))
            writeFile = client.recv(SIZE)
            data = writeFile.decode(FORMAT)
            print(writeFile.decode(FORMAT))
            #if data == 't':
            #    file = open(dir_path.joinpath(file_name), 'a+')
            #    file.write(f"[СЕРВЕР] Файл открыт клиентом '{threading.get_ident()}' в {datetime.now().time()}\n")
            #    timer(5)
            #    file.write(f"[СЕРВЕР] Файл закрыт клиентом '{threading.get_ident()}' в {datetime.now().time()}\n\n")
            #    print(f"\033[32m[СЕРВЕР] Клиент '{threading.get_ident()}' произвел запись в файл\033[0m")
            #    file.close()
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"{msg}")

if __name__ == "__main__":
    main()
