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
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))

        print(f"Connexion établie avec le serveur sur le port {self.port}")

        self.register()
        self.prompt()

        print("Fermeture de la connexion")
        self.connection.close()

    def register(self):
        message = ""
        while message != self.command("NAME"):
            message = self.connection.recv(1024)

        self.connection.send(self.command("StilexHuminex"))

    def prompt(self):
        to_send = ""

        while to_send != b"fin":
            to_send = input(">> ")
            to_send += '\r\n'
            to_send = to_send.encode()
            self.connection.send(to_send)

            msg_recu = self.connection.recv(1024)
            print("<< " + msg_recu.decode())
 

runner = GameInteraction("localhost", 2121)
runner()
