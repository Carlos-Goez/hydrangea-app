import socket
import json
import base64

HOST, PORT = "localhost", 8400


class ServicesMachine:
    @staticmethod
    def send_flower_data(type_request, order , number_flower):
        m = {"type": type_request, "order": order, "number_flower": number_flower}
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
    def send_image(type_request, order, number_flower, path_image):
        file = path_image
        data = {"type": type_request, "order": order, "number_flower": number_flower}
        with open(file, 'rb') as image:
            image_read = image.read()
            image_64_encode = base64.encodebytes(image_read)
            data['image'] = image_64_encode.decode('utf-8')

        with open('data.json', 'w') as active_file:
            json.dump(data, active_file)

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            with open('data.json', 'rb') as f:
                print('send data')
                sock.sendfile(f)

            # Receive data from the server and shut down
            received = sock.recv(1024)
            received = received.decode("utf-8")

        finally:
            sock.close()

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))


ServicesMachine.send_image('rgb', '10001', '1', '/home/agoez/Pictures/rgb_blue.png')