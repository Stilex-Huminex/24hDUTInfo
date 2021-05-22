import socket
import numpy as np


class GameInteraction:

    host = None
    port = None
    connection = None
    team_id = None
    map = None
    pa = None
    can_play = None

    @staticmethod
    def command(name: str):
        return f"{name}\r\n".encode()

    @staticmethod
    def parsename(command: bytes):
        c = command.replace(b"\r\n", b"")
        c = c.decode()
        return c if "|" not in c else c.split('|')[0]

    @staticmethod
    def parseparams(command: bytes):
        c = command.replace(b"\r\n", b"")
        c = c.decode()
        return [] if "|" not in c else c.split('|')[1:]

    def prettify_command(self, command: bytes):
        return [self.parsename(command), self.parseparams(command)]

    @staticmethod
    def plateauToMatrice(plateau: str):
        plateau = ','.join(plateau[i:i+31] for i in range(0, len(plateau), 31))
        tab = plateau.split(',')
        arr = []
        for string in tab:
            arrNp = np.frombuffer(string.encode(), dtype='S1', count=-1)
            arr2 = []
            
            for s in arrNp:
                arr2.append(s.decode())
            arr.append(arr2)
        return arr

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pa = 8
        self.can_play = True

    def __enter__(self):
        # Connect to the game socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))
        print(f"Connexion établie avec le serveur sur le port {self.port}")

        # Register
        self.wait_for_server_command("NAME")
        self.connection.send(self.command("StilexHuminex"))
        print("NAME recieved and answered")

        # Wait for start
        self.team_id = self.wait_for_server_command("START")[0]
        print(f"START detected, team ID is {self.team_id}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close connection
        print("Fermeture de la connexion")
        self.connection.close()

    def __call__(self, command: str):
        if command.startswith("TAKE") or command.startswith("MOVE") or command.startswith("DELIVER"):
            if self.pa == 0:
                self.end_turn()
                return ['OUT', []]  # Prevent action
            else:
                self.pa -= 1
        
        # Interact with the game
        self.connection.send(self.command(command))
        recieved = self.connection.recv(1024)
        infos = self.prettify_command(recieved)
        
        if command == "GETMAP":
            self.map = self.plateauToMatrice(infos[1][0])

        return infos

    def end_turn(self):
        try:
            self.connection.send(self.command("ENDTURN"))
            self.wait_for_server_command("OK")
            self.wait_for_server_command(["START", "ENDGAME"])
        except (ConnectionAbortedError, OSError):
            self.can_play = False

    def wait_for_server_command(self, command):
        message = b""
        if isinstance(command, list):
            c = [self.command(comm) for comm in command]
            while self.parsename(message) not in c:
                message = self.connection.recv(1024)
                return self.parseparams(message)
        else:
            while self.parsename(message) != self.command(command):
                message = self.connection.recv(1024)
                return self.parseparams(message)

    def get_map_pos(self, pos, shift_x=0, shift_y=0):
        return self.map[pos[0]+shift_x][pos[1]+shift_y]
