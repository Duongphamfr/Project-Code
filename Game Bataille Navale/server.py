import pickle
import socket
from _thread import *
import index

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.gethostname()
port = 9999

server_ip = socket.gethostbyname('localhost')

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
player = 0

def threaded_client(conn, player):
    conn.send(str.encode(str(player)))

    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                print("Code dont excuted")
                break
            else:
                if data == "reset":
                    game.reset()
                elif data != "get":
                    game.play(player, data) # data la grid
                
                conn.sendall(pickle.dumps(game))

        except Exception as e:
            print(e)
            break

    print("Connection Closed")
    conn.close()

def main():
    global game, player
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        if player == 0:
            game = index.Game()
            print("Player 1 connected")
            player += 1
        else:
            game.bothConnected = True
            player = 1
            print("Player 2 connected")

        start_new_thread(threaded_client, (conn, player))

if __name__ == '__main__':
    main()