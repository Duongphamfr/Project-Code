import pickle
import socket
from _thread import *
import index

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.gethostname()
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
player = 0

def threaded_client(conn, player):
    conn.send(str.encode(player))

    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                if data == "reset":
                    game.reset()
                elif data != "get":
                    game.play(player, data) # data la grid
                
                conn.sendall(pickle.dumps(game))
                
        except:
            break

    print("Connection Closed")
    conn.close()

def main():
    global game 
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        if player == 0:
            game = index.Game()
            print("Creating a new game...")
        else:
            game.bothConnected = True
            player = 1

        start_new_thread(threaded_client, (conn, player))

if __name__ == '__main__':
    main()