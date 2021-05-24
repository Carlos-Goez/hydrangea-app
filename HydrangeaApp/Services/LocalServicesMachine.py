import socket
import json

HOST, PORT = "localhost", 8400


class LocalService:

    @staticmethod
    def send_start_signal():
        m = {"type": "Start"}
        data = json.dumps(m)
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(data, encoding="utf-8"))

            # Receive data from the server and shut down
            received = sock.recv(1024)
            received = received.decode("utf-8")

        finally:
            sock.close()

        print ("Sent:     {}".format(data))