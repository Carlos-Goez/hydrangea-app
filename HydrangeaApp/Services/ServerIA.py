import socket
import sys
import json
import base64
import asyncio
from HydrangeaApp.temp.captureCamera import CaptureImage
from VisionApp.ValidationOptimized import ClusterFlower
from HydrangeaApp.Services.ClientIA import ServicesData
from HydrangeaApp.temp.image_alignment_simple import AlignImage

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
folder_images = '/home/agoez/Pictures/'
server_name = 'localhost'
server_address = (server_name, 8400)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)


async def execute_classification(path_rgb, path_noir, order, number_flower):
    result = ClusterFlower.predict(path_rgb)
    flower_type = ''
    if result['blue'] == 1:
        flower_type = 'Blue'
    elif result['mini'] == 1:
        flower_type = 'Mini'
    elif result['select'] == 1:
        flower_type = 'Select'
    print(flower_type)
    send_data_classification(flower_type, path_rgb, path_noir, order, number_flower)


def send_data_classification(type_flower, path_rgb, path_noir, order, number_flower):
    ServicesData.send_flower_data(type_flower, order, number_flower, path_rgb, path_noir)


def send_data_align(path_rgb, path_noir, order, number_flower):
    AlignImage.align(path_rgb, path_noir)


while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    CHUNK_SIZE = 20 * 1024
    FILE = 'recv_data.json'
    connection.settimeout(1)
    try:
        print('client connected:', client_address)
        with open(FILE, "wb") as f:
            try:
                while True:
                    chunk = connection.recv(CHUNK_SIZE)
                    print('Receive')
                    f.write(chunk)
                    if not chunk:
                        break
            except Exception as e:
                print(e)

        print('received ')
        connection.send('OK'.encode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        connection.close()
        f = open('recv_data.json')
        data_recv = json.load(f)
        msg = data_recv['type']
        if msg == 'noir':
            path_image_noir = folder_images + data_recv['order'] + '-' \
                             + data_recv['type'] + '-' + str(data_recv['number_flower']) + '.png'
            # CaptureImage.main(name_image)
            print(path_image_noir)
        if msg == 'rgb':
            image_64_decode = base64.decodebytes(data_recv['image'].encode('utf-8'))
            path_image_rgb = folder_images + data_recv['order'] + '-' + \
                             'rgb' + '-' + str(data_recv['number_flower']) + '.png'
            path_image_noir = folder_images + data_recv['order'] + '-' + \
                             'noir' + '-' + str(data_recv['number_flower']) + '.png'
            with open(path_image_rgb, 'wb') as image:
                image.write(image_64_decode)
            print(path_image_rgb)
            asyncio.run(execute_classification(path_image_rgb,
                                               path_image_noir,
                                               data_recv['order'],
                                               str(data_recv['number_flower'])))

        print(msg)
