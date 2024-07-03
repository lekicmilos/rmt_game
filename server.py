import socket
from _thread import *
import threading
import configparser

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

config_data = configparser.ConfigParser()
config_data.read("config.ini")
config = config_data["network"]
server = config.get("host")
port = int(config.get("port"))

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection...")

default_pos = ["0:300;400;300;0;0", "1:300;400;300;0;0"]
pos = default_pos

players = [None, None]


def addPlayer(id):
    if players[0] is None:
        players[0] = id
        return "0"
    else:
        players[1] = id
        return "1"


def removePlayer(id):
    players[players.index(id)] = None


def threaded_client(conn):
    global pos

    newId = addPlayer(threading.current_thread().ident)
    conn.send(str.encode(newId))

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:

                arr = reply.split(";")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    removePlayer(threading.current_thread().ident)
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
