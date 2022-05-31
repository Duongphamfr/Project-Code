import pickle
import socket

class Network:

    def __init__(self, ip_addr = None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip_addr == None:
            self.ip_addr = socket.gethostbyname('localhost')
            self.host = str(self.ip_addr) # get IP address
        else:
            self.host = ip_addr
        self.port = 9999
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(100000))
            return reply
        except Exception as e:
            print(e)
