import socket
from _thread import *
import sys
import pickle
from champion import Champion

server = "192.168.142.39"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

players = [None, None]

currentPlayer = 0
def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
    reply = ""
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()
    currentPlayer -= 1

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    if currentPlayer < len(players) - 1:
        currentPlayer += 1
