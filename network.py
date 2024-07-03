import socket
import configparser


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # citanje host i port iz config.ini fajla
        config_data = configparser.ConfigParser()
        config_data.read("config.ini")
        config = config_data["network"]
        self.host = config.get("host")
        self.port = int(config.get("port"))

        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        id = self.client.recv(2048).decode()
        return id

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
