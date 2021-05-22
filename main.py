import socket


class GameInteraction:

    host = None
    port = None
    connection = None

    @staticmethod
    def command(name: str):
        return f"{name}\r\n".encode()

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __call__(self):
        # Connect to the game socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))
        print(f"Connexion établie avec le serveur sur le port {self.port}")

        # Register
        self.wait_for_server_command("NAME")
        self.connection.send(self.command("StilexHuminex"))

        # Wait for start
        self.wait_for_server_command("START")

        # Interact with the game
        self.prompt()

        # Close connection
        print("Fermeture de la connexion")
        self.connection.close()

    def wait_for_server_command(self, command: str):
        message = ""
        while message != self.command(command):
            message = self.connection.recv(1024)

    def prompt(self):
        to_send = ""

        while to_send != b"fin":
            to_send = self.command(input(">> "))
            self.connection.send(to_send)

            msg_recu = self.connection.recv(1024)
            print("<< " + msg_recu.decode())
 

runner = GameInteraction("localhost", 2121)
runner()
