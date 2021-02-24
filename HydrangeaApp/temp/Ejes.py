from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep
from math import pi
import RPi.GPIO as GPIO

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)


def initConfig(): 
    pca.frequency = 700
    for x in range(1, 16):
        pca.channels[x].duty_cycle = 0x0000


class Pinzas():
    def __init__(self, direccion, paso, stop):
        self.direccion = direccion
        self.paso = paso
        self.stop = stop
        self.estado = "OFF"
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(direccion, GPIO.OUT)
        GPIO.setup(paso, GPIO.OUT)
        GPIO.setup(stop, GPIO.IN)

    def POpen(self):
        pca.frequency = 600
        GPIO.output(self.direccion,1)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(0.17)
        pca.channels[self.paso].duty_cycle = 0x0000

    def PStop(self):
        pca.frequency = 700
        GPIO.output(self.direccion,0)
        pca.channels[self.paso].duty_cycle = 0x7fff 
        while (GPIO.input(self.stop)):
            pass
        pca.channels[self.paso].duty_cycle = 0x0000

    def PHome(self):
        pca.frequency = 200
        GPIO.output(self.direccion,0)
        pca.channels[self.paso].duty_cycle = 0x7fff 
        while (GPIO.input(self.stop)):
            pass
        pca.channels[self.paso].duty_cycle = 0x0000

class Rotacional():
    def __init__(self, direccion, paso):
        self.direccion = direccion
        self.paso = paso
        self.grados = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(direccion, GPIO.OUT)
        GPIO.setup(paso, GPIO.OUT)

    def ManualUp(self):
        gradosDown=self.grados+(1.8*5)
        self.GotoGrados(gradosDown,60)

    def ManualDown(self):
        gradosDown=self.grados-(1.8*5)
        self.GotoGrados(gradosDown,60)

    def GotoGrados(self,gradosFinales,frec):
        gradosFaltantes = gradosFinales - self.grados
        pasosFaltantes = round(abs(gradosFaltantes) / 1.8)
        pca.frequency = frec
        tiempoMuerto = (1/frec)*pasosFaltantes
        if gradosFaltantes>0:
            GPIO.output(self.direccion,1)
            self.grados = self.grados + (pasosFaltantes*1.8)
        else:
            GPIO.output(self.direccion,0)
            self.grados = self.grados - (pasosFaltantes*1.8)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(tiempoMuerto)
        pca.channels[self.paso].duty_cycle = 0x0000

    def ResetHome(self):
        self.grados= 0

# diametro translacional 2.8


class Traslacional():
    def __init__(self, direccion, paso, stop):
        self.direccion = direccion
        self.paso = paso
        self.stop = stop
        self.grados = 0
        self.distancia = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(direccion, GPIO.OUT)
        GPIO.setup(paso, GPIO.OUT)
        GPIO.setup(stop, GPIO.IN)

    def ManualUp(self):
        distanciaAux=self.distancia+(20)
        self.GotoDistancia(distanciaAux,60)

    def ManualDown(self):
        distanciaAux=self.distancia-(20)
        self.GotoDistancia(distanciaAux,60)

    def GotoGrados(self,gradosFinales,frec):
        gradosFaltantes = gradosFinales - self.grados
        pasosFaltantes = round(abs(gradosFaltantes) / 1.8)
        pca.frequency = frec
        tiempoMuerto = (1/frec)*pasosFaltantes
        if gradosFaltantes>0:
            GPIO.output(self.direccion,1)
            self.grados = self.grados + (pasosFaltantes*1.8)
        else:
            GPIO.output(self.direccion,0)
            self.grados = self.grados - (pasosFaltantes*1.8)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(tiempoMuerto)
        pca.channels[self.paso].duty_cycle = 0x0000

    def GotoDistancia(self,distanciaFinal,frec):
        #Convertir distancia faltante en distancia final
        # 90 mm avanza 360 grados
        distanciaFaltante = distanciaFinal - self.distancia
        gradosFaltantes = (distanciaFaltante/14)*(180/pi)
        gradosPut=self.grados+(gradosFaltantes)
        self.GotoGrados(gradosPut,frec)
        self.distancia = self.grados*(pi/180)*14

    def ResetHome(self):
        pca.frequency = 350
        GPIO.output(self.direccion,0)
        pca.channels[self.paso].duty_cycle = 0x7fff 
        while (GPIO.input(self.stop)):
            pass
        pca.channels[self.paso].duty_cycle = 0x0000
        self.grados = 0
        self.distancia = 0


class Elevador():
    def __init__(self, direccion, paso, stop):
        self.direccion = direccion
        self.paso = paso
        self.stop = stop
        self.grados = 0
        self.distancia = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(direccion, GPIO.OUT)
        GPIO.setup(paso, GPIO.OUT)
        GPIO.setup(stop, GPIO.IN)

    def ManualUp(self):
        distanciaAux=self.distancia+(90)
        self.GotoDistancia(distanciaAux,60)

    def ManualDown(self):
        distanciaAux=self.distancia-(90)
        self.GotoDistancia(distanciaAux,60)

    def GotoGrados(self,gradosFinales,frec):
        gradosFaltantes = gradosFinales - self.grados
        pasosFaltantes = round(abs(gradosFaltantes) / 1.8)
        pca.frequency = frec
        tiempoMuerto = (1/frec)*pasosFaltantes
        if gradosFaltantes>0:
            GPIO.output(self.direccion,1)
            self.grados = self.grados + (pasosFaltantes*1.8)
        else:
            GPIO.output(self.direccion,0)
            self.grados = self.grados - (pasosFaltantes*1.8)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(tiempoMuerto)
        pca.channels[self.paso].duty_cycle = 0x0000

    def GotoDistancia(self,distanciaFinal,frec):
        #Convertir distancia faltante en distancia final
        # 90 mm avanza 360 grados
        distanciaFaltante = distanciaFinal - self.distancia
        gradosFaltantes = (distanciaFaltante/14)*(180/pi)
        gradosPut=self.grados+(gradosFaltantes)
        self.GotoGrados(gradosPut,frec)
        self.distancia = self.grados*(pi/180)*14

    def ResetHome(self):
        pca.frequency = 300
        GPIO.output(self.direccion,1)
        pca.channels[self.paso].duty_cycle = 0x7fff 
        while (GPIO.input(self.stop)):
            pass
        pca.channels[self.paso].duty_cycle = 0x0000
        self.grados = 0
        self.distancia = 0
        