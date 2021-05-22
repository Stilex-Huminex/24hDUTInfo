import socket
import numpy as np


class GameInteraction:

    host = None
    port = None
    connection = None
    team_id = None
    map = None
    pa = None

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

    def __call__(self, command: str):
        
        # Interact with the game
        self.connection.send(self.command(command))
        infos = self.prettify_command(self.connection.recv(1024))
        
        if (command == "GETMAP"):
            self.map = self.plateauToMatrice(infos[1][0])
        if (command.startswith("TAKE") or command.startswith("MOVE") or command.startswith("DELIVER")):
            self.pa -= 1
            if self.pa == 0:
                self.connection.send(self.command("ENDTURN"))
                self.pa = 8


        return infos

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

    def wait_for_server_command(self, command: str):
        message = b""
        while self.parsename(message) != self.command(command):
            message = self.connection.recv(1024)
            return self.parseparams(message)