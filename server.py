import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("منتظر برقراری ارتباط... , سرور استارت شد")

# "connected" store ip addresses
connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)  # "data" can be player move

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("قطع ارتباط !")
    try:
        del games[gameId]
        print("درحال بستن بازی...", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("متصل شد به :", addr)
    idCount += 1
    p = 0  # for current player

    gameId = (idCount - 1) // 2  # increase id by 1 when 2 ips connect
    if idCount % 2 == 1:  # if we did'nt have a pair for a new player
        games[gameId] = Game(gameId)
        print("در حال ساخت بازی جدید...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
