import socket


class GameInteraction:

    host = None
    port = None
    connection = None
    team_id = None

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

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __call__(self, command: str):
        # Interact with the game
        self.connection.send(self.command(command))
        return self.prettify_command(self.connection.recv(1024))

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
 

with GameInteraction("localhost", 2121) as runner:
    print(runner('GETMAP'))
