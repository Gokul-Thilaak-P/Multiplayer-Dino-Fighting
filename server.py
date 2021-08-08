import socket
import threading
import pickle
from player import Player

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDRESS = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)
game_id = -1
after_a_game = [Player(1, 100, 325, 75, 75, "Dino-Gr", False),
                Player(2, 788, 325, 75, 75, "Dino-Bl", False)]
players = {-1: after_a_game.copy()}


def handle_clients(conn, player, g_id):
    try:
        print(f"game_id: {g_id}, index : {player}")
        conn.send(pickle.dumps(players[g_id][player]))
        while True:
            players[g_id][player] = pickle.loads(conn.recv(2048))
            if player == 0:
                conn.send(pickle.dumps(players[g_id][1]))
            else:
                conn.send(pickle.dumps(players[g_id][0]))

    except EOFError:
        players[g_id][player].ready_to_play = False
        players[g_id][player].is_connected = False
        players[g_id][player].is_game_over = True

        print(f"Player {players[g_id][player].id} from game {g_id} Disconnected...")
        if g_id in players:
            if players[g_id][(player + 1) % 2].is_game_over and players[g_id][player].is_game_over:
                players.pop(g_id)


def start():
    global game_id
    print(f"Server is Started by {SERVER} \nWaiting for connection...")
    s.listen()
    while True:
        c, address = s.accept()

        after_a_game[0].is_connected = False
        after_a_game[1].is_connected = False
        try:
            if players[game_id][0].is_connected:  # If p1 is connected. We give the index of p2
                player = 1

            elif players[game_id][1].is_connected:  # If p2 is connected. We give the index of p1
                player = 0
            else:
                game_id += 1
                player = 0
                players[game_id] = after_a_game.copy()

            if players[game_id][0].is_connected and players[game_id][1].is_connected:
                game_id += 1
                player = 0
                players[game_id] = after_a_game.copy()

        except KeyError as key:
            r_key = str(key)
            r_key = int(r_key)
            players[r_key] = after_a_game.copy()
            if players[game_id][0].is_connected:  # If p1 is connected. We give the index of p2
                player = 1
            elif players[game_id][1].is_connected:  # If p2 is connected. We give the index of p1
                player = 0
            else:
                game_id += 1
                player = 0
                players[game_id] = after_a_game.copy()

            if players[game_id][0].is_connected and players[game_id][1].is_connected:
                game_id += 1
                player = 0
                players[game_id] = after_a_game.copy()

            if r_key in players:
                players.pop(r_key)

        if -1 in players:
            players.pop(-1)

        print(f"Games Active : {len(players)}")

        players[game_id][player].is_connected = True
        thread = threading.Thread(target=handle_clients, args=(c, player, game_id))
        thread.start()  # Thread Increases here...
        print(f"\nConnections : {threading.active_count() - 1}")


start()
