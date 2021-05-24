import socket
import json

HOST, PORT = "localhost", 8300


class ServicesData:
    @staticmethod
    def send_flower_data(type_flower, order, number_flower, path_rgb, path_noir):

        m = {"type": type_flower,
             "order": order,
             "number_flower": number_flower,
             "path_rgb": path_rgb,
             "path_noir": path_noir}
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
        print ("Received: {}".format(received))

    @staticmethod
    def send_ndvi_gci(order, number_flower, ndvi, gci, path_ndvi, path_gci):

        m = {"type": 'ndvi_gci',
             "order": order,
             "number_flower": number_flower,
             "ndvi": ndvi,
             "gci": gci,
             "path_ndvi": path_ndvi,
             "path_gci": path_gci}

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

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))

