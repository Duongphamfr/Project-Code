import socket

class Network:

    def __init__(self, ip_addr = None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip_addr == None:
            self.hostname = socket.gethostname()
            self.ip_addr = socket.gethostbyname((self.hostname))
            self.host = str(self.ip_addr) # get IP address
        else:
            self.host = ip_addr
        self.port = 6803
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)