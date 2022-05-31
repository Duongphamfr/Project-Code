import pickle
import socket

class Network:
    def __init__(self, ip_addr = None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # use a socket to send and receive UDP data from an IPv4 address
        if ip_addr == None: # player 1 create a server on his computer
            self.ip_addr = socket.gethostbyname('localhost')
            self.host = str(self.ip_addr) # get local IP address of players's computer
        else: # player 2 create a connection to a server using the IP address
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

    # send data to server (dumps data into binary) and get back the new game data
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(100000))
            return reply
        except Exception as e:
            print(e)
