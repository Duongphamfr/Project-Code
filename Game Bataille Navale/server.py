import pickle
import socket
from _thread import *
from turtle import update
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
playerId = 0

def threaded_client(conn, playerId):
    conn.send(str.encode(str(playerId)))

    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(100000))
            if not data:
                print("Code dont excuted")
                break
            else:
                if data == "reset":
                    game.reset()
                elif data == "small" or data == "medium":
                    game.setSize(data)
                elif data == "ready":
                    game.setReady(playerId)
                elif data == "1" or data == "2":
                    game.setWinner(int(data))
                elif data == "pushed grid":
                    game.setPushGrid(playerId)
                elif data == "toggle grid":
                    game.toggleGrid = True
                elif data == "turn 1" or data == "turn 2":
                    if data == "turn 1":
                        game.setTurn(1)
                    else:
                        game.setTurn(2)


                elif isinstance(data, str) and data != "update":
                    game.setName(playerId, data)
                elif data != "update":
                    if not game.toggleGrid:
                        if playerId == 1:
                            game.setGrid(playerId, data)
                        else:
                            game.setGrid(playerId, data)
                    else:
                        if playerId == 1:
                            game.updateGrid2 = data
                        else:
                            game.updateGrid1 = data
                            
                conn.sendall(pickle.dumps(game))

        except Exception as e:
            print(e)
            break

    print("Connection Closed")
    conn.close()

def main():
    global game, playerId
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        playerId += 1

        if playerId == 1:
            game = index.Game()
            print("Player 1 connected")
        else:
            game.bothConnected = True
            playerId = 2
            print("Player 2 connected")

        start_new_thread(threaded_client, (conn, playerId))


if __name__ == '__main__':
    main()