#from picamera import PiCamera
#from time import sleep
#import sys
import time

# ahora = time.strftime("%c")


class CaptureImage:

    @staticmethod
    def main(path):
        camera = PiCamera()
        camera.resolution = (600, 480)
        camera.framerate = 15
        gains = (.74, 4.12)
        camera.start_preview()
        sleep(1)
        name_image = path
        print(name_image)
        camera.capture(name_image)
        camera.stop_preview()
        return name_image