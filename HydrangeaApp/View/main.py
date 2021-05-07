# -*-coding utf-8-*-

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.list import MDList
from HydrangeaApp.Controllers.Session import Session
from HydrangeaApp.Controllers.ApplicationController import DataController
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomnavigation import MDBottomNavigation
import re


# import _thread
# import Ejes
# traslX = Ejes.Traslacional(4,10,16)
# traslY = Ejes.Traslacional(5,11,17)
# traslZ = Ejes.Elevador(6,12,18)
# rotY = Ejes.Rotacional(8,13)
# rotX = Ejes.Rotacional(13,14)
# #rotX = Ejes.Rotacional(11,15)
# pinzas = Ejes.Pinzas(11,15,19)

current_session = Session()


class WindowsManager(ScreenManager):
    def check_admin(self):
        if current_session.get_role() != 1:
            self.current = 'Screen Login'


class BottomNavigationHome(MDBottomNavigation):
    def check_admin(self):
        if current_session.get_role() != '1':
            self.switch_tab('home')


class ScreenSignup(Screen):
    def on_enter(self, *args):
        self.check_admin()

    def check_admin(self):
        if current_session.get_role() != '1':
            self.parent.current = 'Screen Login'


class ScreenHome(Screen):
    pass


class ListMenu(MDList):
    def logout(self):
        self.parent.parent.parent.parent.parent.ids.bottom_navigation.switch_tab('home')
        current_session.set_role(None)
        current_session.set_username(None)


class Home(BoxLayout):
    pass


class Order(BoxLayout):
    pass


class Stats(BoxLayout):
    pass


class History(BoxLayout):
    pass


class Setting(BoxLayout):
    pass


class Toolbar(MDToolbar):
    pass


class Login(BoxLayout):
    def create_session(self):
        user = self.ids['field_user'].text
        password = self.ids['password_layout'].ids['field_password'].text

        self.check_username(user, password)

    def check_username(self, username, password):
        username_text = username
        password_text = password
        username_check_false = False

        if not re.match("^[a-zA-z0-9]", username):
            username_check_false = True
        if username_check_false or username_text.split() == [] or password_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Dato Invalido',
                text="Por favor ingrese una clave y usuario validos",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            if DataController.login(username, password, current_session):
                self.parent.parent.parent.parent.ids["bottom_navigation"].switch_tab('home')
                self.parent.parent.current = 'Screen Home'
            else:
                cancel_btn_username_dialogue = MDFlatButton(
                    text='Cerrar', on_release=self.close_username_dialogue)
                self.dialog = MDDialog(
                    title='Algo salio mal',
                    text="Por favor verifique su usuario y contraseña",
                    size_hint=(0.7, 0.2),
                    buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
        self.ids['field_user'].text = ''
        self.ids['password_layout'].ids['field_password'].text = ''

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()


class SignUp(BoxLayout):
    def create_user(self):
        user = self.ids['field_register_user'].text
        password = self.ids.password_layout.ids.field_password.text
        role = self.ids['check_register_role'].active
        self.check_username(user, password, role)

    def check_username(self, username, password, role):

        username_text = username
        password_text = password
        username_check_false = False

        if not re.match("^[a-zA-z0-9]", username):
            username_check_false = True
        if username_check_false or username_text.split() == [] or password_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Dato Invalido',
                text="Por favor ingrese una clave y usuario validos",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            notice = DataController.singup(username, password, 1 if role else 2)
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Aviso',
                text=notice,
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

        self.ids['field_register_user'].text = ''
        self.ids.password_layout.ids.field_password.text = ''
        self.ids['check_register_role'].active = False

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class DataTable(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__()
        data_tables = MDDataTable(
            size_hint=(0.9, .9),
            # name column, width column
            column_data=[
                ("#", dp(8)),
                ("Pedido", dp(30)),
                ("T.Caja", dp(20)),
                ("Mini", dp(20)),
                ("Selecta", dp(20)),
                ("Azul", dp(20)),
                ("Estado", dp(20)),
                ("%Completado", dp(25)),
            ],
        )
        self.add_widget(data_tables)


class DataTableHistory(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__()
        data_tables = MDDataTable(
            size_hint=(0.9, .9),
            # name column, width column
            column_data=[
                ("#", dp(8)),
                ("Pedido", dp(30)),
                ("T.Caja", dp(20)),
                ("Mini", dp(20)),
                ("Selecta", dp(20)),
                ("Azul", dp(20)),
                ("Estado", dp(20)),
                ("%Completado", dp(25)),
            ],
        )
        self.add_widget(data_tables)


class ClickableTextFieldRound(RelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class DataTableOrderActive(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__()
        data_tables = MDDataTable(
            size_hint=(0.9, .9),
            # name column, width column
            column_data=[
                ("#", dp(8)),
                ("Pedido", dp(30)),
                ("T.Caja", dp(20)),
                ("Mini", dp(20)),
                ("Selecta", dp(20)),
                ("Azul", dp(20)),
                ("Estado", dp(20)),
                ("%Completado", dp(25)),
            ],
        )
        self.add_widget(data_tables)


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.home = 0
        self.cols = 6
        self.padding = [dp(15), dp(15)]
        self.spacing = [dp(10), dp(10)]

        # Position control axis X
        self.add_widget(MDLabel(text="X", halign="center", font_style='H5'))
        self.Xtxt = TextInput(multiline=False, halign="center")
        self.add_widget(self.Xtxt)
        self.BtnUpX = Button(text="UP")
        # self.BtnUpX.bind(on_press=self.XBtnUp)
        self.add_widget(self.BtnUpX)
        self.BtnDownX = Button(text="DOWN")
        # self.BtnDownX.bind(on_press=self.XBtnDown)
        self.add_widget(self.BtnDownX)
        self.BtnResetX = Button(text="Reset")
        # self.BtnResetX.bind(on_press=self.XBtnReset)
        self.add_widget(self.BtnResetX)
        self.BtnGotoX = Button(text="Go to")
        # self.BtnGotoX.bind(on_press=self.XBtnGoto)
        self.add_widget(self.BtnGotoX)

        self.add_widget(MDLabel(text="Y", halign="center", font_style='H5'))
        self.Ytxt = TextInput(multiline=False, halign="center")
        self.add_widget(self.Ytxt)
        self.BtnUpY = Button(text="UP")
        # self.BtnUpY.bind(on_press=self.YBtnUp)
        self.add_widget(self.BtnUpY)
        self.BtnDownY = Button(text="DOWN")
        # self.BtnDownY.bind(on_press=self.YBtnDown)
        self.add_widget(self.BtnDownY)
        self.BtnResetY = Button(text="Reset")
        # self.BtnResetY.bind(on_press=self.YBtnReset)
        self.add_widget(self.BtnResetY)
        self.BtnGotoY = Button(text="Go to")
        # self.BtnGotoY.bind(on_press=self.YBtnGoto)
        self.add_widget(self.BtnGotoY)

        self.add_widget(MDLabel(text="Z", halign="center", font_style='H5'))
        self.Ztxt = TextInput(multiline=False, halign="center")
        self.add_widget(self.Ztxt)
        self.BtnUpZ = Button(text="UP")
        # self.BtnUpZ.bind(on_press=self.ZBtnUp)
        self.add_widget(self.BtnUpZ)
        self.BtnDownZ = Button(text="DOWN")
        # self.BtnDownZ.bind(on_press=self.ZBtnDown)
        self.add_widget(self.BtnDownZ)
        self.BtnResetZ = Button(text="Reset")
        # self.BtnResetZ.bind(on_press=self.ZBtnReset)
        self.add_widget(self.BtnResetZ)
        self.BtnGotoZ = Button(text="Go to")
        # self.BtnGotoZ.bind(on_press=self.ZBtnGoto)
        self.add_widget(self.BtnGotoZ)

        self.add_widget(MDLabel(text="RotY", halign="center", font_style='H5'))
        self.RotYtxt = TextInput(multiline=False, halign="center")
        self.add_widget(self.RotYtxt)
        self.BtnUpRotY = Button(text="UP")
        # self.BtnUpRotY.bind(on_press=self.RotYBtnUp)
        self.add_widget(self.BtnUpRotY)
        self.BtnDownRotY = Button(text="DOWN")
        # self.BtnDownRotY.bind(on_press=self.RotYBtnDown)
        self.add_widget(self.BtnDownRotY)
        self.BtnResetRotY = Button(text="Reset")
        # self.BtnResetRotY.bind(on_press=self.RotYBtnReset)
        self.add_widget(self.BtnResetRotY)
        self.BtnGotoRotY = Button(text="Go to")
        # self.BtnGotoRotY.bind(on_press=self.RotYBtnGoto)
        self.add_widget(self.BtnGotoRotY)

        self.add_widget(MDLabel(text="RotX", halign="center", font_style='H5'))
        self.RotXtxt = TextInput(multiline=False, halign="center")
        self.add_widget(self.RotXtxt)
        self.BtnUpRotX = Button(text="UP")
        # self.BtnUpRotX.bind(on_press=self.RotXBtnUp)
        self.add_widget(self.BtnUpRotX)
        self.BtnDownRotX = Button(text="DOWN")
        # self.BtnDownRotX.bind(on_press=self.RotXBtnDown)
        self.add_widget(self.BtnDownRotX)
        self.BtnResetRotX = Button(text="Reset")
        # self.BtnResetRotX.bind(on_press=self.RotXBtnReset)
        self.add_widget(self.BtnResetRotX)
        self.BtnGotoRotX = Button(text="Go to")
        # self.BtnGotoRotX.bind(on_press=self.RotXBtnGoto)
        self.add_widget(self.BtnGotoRotX)

        self.add_widget(
            MDLabel(text="Pinzas", halign="center", font_style='H5'))
        self.Gripper = Button(text="ON")
        # self.Gripper.bind(on_press=self.GripperPressed)
        self.add_widget(self.Gripper)
        self.GripperHome = Button(text="Home")
        # self.GripperHome.bind(on_press=self.GripperPressedHome)
        self.add_widget(self.GripperHome)


""" def GripperPressed(self, instance): if self.home == 1:
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
"""


class MainApp(MDApp):
    def build(self):
        self.title = "HydrangeaApp"
        self.theme_cls.primary_palette = "Indigo"

    def on_start(self):
        self.root.ids.screen_manager.current = 'Screen Login'


if __name__ == "__main__":
    MainApp().run()
    # Ejes.initConfig()
