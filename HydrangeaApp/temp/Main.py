from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import _thread
import Ejes

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')
traslX = Ejes.Traslacional(4,10,16)
traslY = Ejes.Traslacional(5,11,17)
traslZ = Ejes.Elevador(6,12,18)
rotY = Ejes.Rotacional(8,13)
rotX = Ejes.Rotacional(13,14)
# rotX = Ejes.Rotacional(11,15)
pinzas = Ejes.Pinzas(11,15,19)

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep
from math import pi0
import RPi.GPIO as GPIO
import time

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)

def initConfig():
    pca.frequency = 700
    for x in range(1, 16):
        pca.channels[x].duty_cycle = 0x0000

class Pinzas():
    def __init__(self, direccion, paso, stop, sensor):
        self.direccion = direccion
        self.paso = paso
        self.stop = stop
        self.estado = "OFF"
        self.sensor = sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(direccion, GPIO.OUT)
        GPIO.setup(paso, GPIO.OUT)
        GPIO.setup(stop, GPIO.IN)
        GPIO.setup(sensor, GPIO.IN)

    def POpen(self):
        pca.frequency = 200
        GPIO.output(self.direccion,1)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(0.7)
        pca.channels[self.paso].duty_cycle = 0x0000
    def PStop(self):
        pca.frequency = 200
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
        self.Listen()

    def Listen(self):
        while (GPIO.input(self.sensor)==1):
            print("nada que me llega")
            time.sleep(1)
        print("esto es una belleza")

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

class RotacionalPlanterios():
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
        pasosFaltantes = round(abs(gradosFaltantes) / 1.8)*3
        pca.frequency = frec
        tiempoMuerto = (1/frec)*pasosFaltantes
        if gradosFaltantes>0:
            GPIO.output(self.direccion,0)
            self.grados = self.grados + ((pasosFaltantes/3)*1.8)
        else:
            GPIO.output(self.direccion,1)
            self.grados = self.grados - ((pasosFaltantes/3)*1.8)
        pca.channels[self.paso].duty_cycle = 0x7fff
        sleep(tiempoMuerto)
        pca.channels[self.paso].duty_cycle = 0x0000
    def ResetHome(self):
        self.grados= 0

#diametro translacional 2.8
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
        distanciaAux=self.distancia+(8)
        self.GotoDistancia(distanciaAux,60)
    def ManualDown(self):
        distanciaAux=self.distancia-(8)
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
        # 8 mm avanza 360 grados
        distanciaFaltante = distanciaFinal - self.distancia
        gradosFaltantes = distanciaFaltante*(360/8)
        gradosPut=self.grados+(gradosFaltantes)
        self.GotoGrados(gradosPut,frec)
        self.distancia = self.grados*(8/360)
    def ResetHome(self):
        pca.frequency = 350
        GPIO.output(self.direccion,1)
        pca.channels[self.paso].duty_cycle = 0x7fff
        while (GPIO.input(self.stop)):
            pass
        pca.channels[self.paso].duty_cycle = 0x0000
        self.grados = 0
        self.distancia = 0
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.home = 0
        self.cols = 6

        self.add_widget(Label(text="X"))
        self.Xtxt = TextInput(multiline=False)
        self.add_widget(self.Xtxt)
        self.BtnUpX = Button(text="UP")
        self.BtnUpX.bind(on_press=self.XBtnUp)
        self.add_widget(self.BtnUpX)
        self.BtnDownX = Button(text="DOWN")
        self.BtnDownX.bind(on_press=self.XBtnDown)
        self.add_widget(self.BtnDownX)
        self.BtnResetX = Button(text="Reset")
        self.BtnResetX.bind(on_press=self.XBtnReset)
        self.add_widget(self.BtnResetX)
        self.BtnGotoX = Button(text="Go to")
        self.BtnGotoX.bind(on_press=self.XBtnGoto)
        self.add_widget(self.BtnGotoX)

        self.add_widget(Label(text="Y"))
        self.Ytxt = TextInput(multiline=False)
        self.add_widget(self.Ytxt)
        self.BtnUpY = Button(text="UP")
        self.BtnUpY.bind(on_press=self.YBtnUp)
        self.add_widget(self.BtnUpY)
        self.BtnDownY = Button(text="DOWN")
        self.BtnDownY.bind(on_press=self.YBtnDown)
        self.add_widget(self.BtnDownY)
        self.BtnResetY = Button(text="Reset")
        self.BtnResetY.bind(on_press=self.YBtnReset)
        self.add_widget(self.BtnResetY)
        self.BtnGotoY = Button(text="Go to")
        self.BtnGotoY.bind(on_press=self.YBtnGoto)
        self.add_widget(self.BtnGotoY)

        self.add_widget(Label(text="Z"))
        self.Ztxt = TextInput(multiline=False)
        self.add_widget(self.Ztxt)
        self.BtnUpZ = Button(text="UP")
        self.BtnUpZ.bind(on_press=self.ZBtnUp)
        self.add_widget(self.BtnUpZ)
        self.BtnDownZ = Button(text="DOWN")
        self.BtnDownZ.bind(on_press=self.ZBtnDown)
        self.add_widget(self.BtnDownZ)
        self.BtnResetZ = Button(text="Reset")
        self.BtnResetZ.bind(on_press=self.ZBtnReset)
        self.add_widget(self.BtnResetZ)
        self.BtnGotoZ = Button(text="Go to")
        self.BtnGotoZ.bind(on_press=self.ZBtnGoto)
        self.add_widget(self.BtnGotoZ)

        self.add_widget(Label(text="RotY"))
        self.RotYtxt = TextInput(multiline=False)
        self.add_widget(self.RotYtxt)
        self.BtnUpRotY = Button(text="UP")
        self.BtnUpRotY.bind(on_press=self.RotYBtnUp)
        self.add_widget(self.BtnUpRotY)
        self.BtnDownRotY = Button(text="DOWN")
        self.BtnDownRotY.bind(on_press=self.RotYBtnDown)
        self.add_widget(self.BtnDownRotY)
        self.BtnResetRotY = Button(text="Reset")
        self.BtnResetRotY.bind(on_press=self.RotYBtnReset)
        self.add_widget(self.BtnResetRotY)
        self.BtnGotoRotY = Button(text="Go to")
        self.BtnGotoRotY.bind(on_press=self.RotYBtnGoto)
        self.add_widget(self.BtnGotoRotY)

        self.add_widget(Label(text="RotX"))
        self.RotXtxt = TextInput(multiline=False)
        self.add_widget(self.RotXtxt)
        self.BtnUpRotX = Button(text="UP")
        self.BtnUpRotX.bind(on_press=self.RotXBtnUp)
        self.add_widget(self.BtnUpRotX)
        self.BtnDownRotX = Button(text="DOWN")
        self.BtnDownRotX.bind(on_press=self.RotXBtnDown)
        self.add_widget(self.BtnDownRotX)
        self.BtnResetRotX = Button(text="Reset")
        self.BtnResetRotX.bind(on_press=self.RotXBtnReset)
        self.add_widget(self.BtnResetRotX)
        self.BtnGotoRotX = Button(text="Go to")
        self.BtnGotoRotX.bind(on_press=self.RotXBtnGoto)
        self.add_widget(self.BtnGotoRotX)

        self.add_widget(Label(text="Pinzas"))
        self.Gripper = Button(text="ON")
        self.Gripper.bind(on_press=self.GripperPressed)
        self.add_widget(self.Gripper)
        self.GripperHome = Button(text="Home")
        self.GripperHome.bind(on_press=self.GripperPressedHome)
        self.add_widget(self.GripperHome)

    def GripperPressed(self, instance):
        if self.home == 1:
            if self.Gripper.text == "ON":
                _thread.start_new_thread(pinzas.POpen,())
                self.Gripper.text = "OFF"
            else:
                _thread.start_new_thread(pinzas.PStop,())
                self.Gripper.text = "ON"
        else:
            print ("Home primero")

    def GripperPressedHome(self, instance):
        pinzas.PHome()
        self.home = 1

    def RotXBtnUp(self, instance):
        rotX.ManualUp()
        self.RotXtxt.text = str(rotX.grados)
    def RotXBtnDown(self, instance):
        rotX.ManualDown()
        self.RotXtxt.text = str(rotX.grados)
    def RotXBtnGoto(self, instance):
        GoRotX=int(self.RotXtxt.text)
        rotX.GotoGrados(GoRotX,80)
        self.RotXtxt.text = str(rotX.grados)
    def RotXBtnReset(self, instance):
        rotX.ResetHome()
        self.RotXtxt.text = str(rotX.grados)

    def RotYBtnUp(self, instance):
        rotY.ManualUp()
        self.RotYtxt.text = str(rotY.grados)
    def RotYBtnDown(self, instance):
        rotY.ManualDown()
        self.RotYtxt.text = str(rotY.grados)
    def RotYBtnGoto(self, instance):
        GoRotY=int(self.RotYtxt.text)
        rotY.GotoGrados(GoRotY,80)
        self.RotYtxt.text = str(rotY.grados)
    def RotYBtnReset(self, instance):
        rotY.ResetHome()
        self.RotYtxt.text = str(rotY.grados)

    def XBtnUp(self, instance):
        traslX.ManualUp()
        self.Xtxt.text = str(traslX.distancia)
    def XBtnDown(self, instance):
        traslX.ManualDown()
        self.Xtxt.text = str(traslX.distancia)
    def XBtnGoto(self, instance):
        GoX=int(self.Xtxt.text)
        traslX.GotoDistancia(GoX,300)
        self.Xtxt.text = str(traslX.distancia)
    def XBtnReset(self, instance):
        traslX.ResetHome()
        self.Xtxt.text = str(traslX.distancia)

    def YBtnUp(self, instance):
        traslY.ManualUp()
        self.Ytxt.text = str(traslY.distancia)
    def YBtnDown(self, instance):
        traslY.ManualDown()
        self.Ytxt.text = str(traslY.distancia)
    def YBtnGoto(self, instance):
        GoY=int(self.Ytxt.text)
        traslY.GotoDistancia(GoY,300)
        self.Ytxt.text = str(traslY.distancia)
    def YBtnReset(self, instance):
        traslY.ResetHome()
        self.Ytxt.text = str(traslY.distancia)

    def ZBtnUp(self, instance):
        traslZ.ManualUp()
        self.Ztxt.text = str(traslZ.distancia)
    def ZBtnDown(self, instance):
        traslZ.ManualDown()
        self.Ztxt.text = str(traslZ.distancia)
    def ZBtnGoto(self, instance):
        GoZ=int(self.Ztxt.text)
        traslZ.GotoDistancia(GoZ,1000)
        self.Ztxt.text = str(traslZ.distancia)
    def ZBtnReset(self, instance):
        traslZ.ResetHome()
        self.Ztxt.text = str(traslZ.distancia)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__=="__main__":
    Ejes.initConfig()
    MyApp().run()