# -*-coding utf-8-*-
# install_twisted_rector must be called before importing and using the reactor

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app

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
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from datetime import datetime

import statistics
import re
import json

PORT = 5920

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
    def on_enter(self, *args):
        Clock.schedule_once(self.check_user)

    def check_user(self, *args):
        if current_session.get_username() is None:
            self.parent.current = 'Screen Login'


class ListMenu(MDList):
    def logout(self):
        self.parent.parent.parent.parent.parent.ids.bottom_navigation.switch_tab('home')
        self.parent.parent.parent.parent.parent.ids.content_drawer.ids.name_account.text = 'None'
        self.parent.parent.parent.parent.parent.ids.content_drawer.ids.role_account.text = 'None'
        current_session.set_role(None)
        current_session.set_username(None)


class Home(BoxLayout):
    def on_kv_post(self, base_widget):
        self.charge_data(self)

    def charge_data(self, *args):
        # Loads data into data grip home
        data_order_machine = DataController.search_orders_inside_machine()
        if len(data_order_machine) >= 1:
            self.ids.data_order_ongoing.ids.order_id.text = str(data_order_machine[0][0])
            self.ids.data_order_ongoing.ids.box_size.text = str(data_order_machine[0][1])
            self.ids.data_order_ongoing.ids.box.text = str(data_order_machine[0][2])
            self.ids.data_order_ongoing.ids.mini.text = str(data_order_machine[0][3])
            self.ids.data_order_ongoing.ids.select.text = str(data_order_machine[0][4])
            self.ids.data_order_ongoing.ids.blue.text = str(data_order_machine[0][5])
            if len(data_order_machine) >= 2:
                self.ids.data_order_outstanding.ids.order_id.text = str(data_order_machine[1][0])
                self.ids.data_order_outstanding.ids.box_size.text = str(data_order_machine[1][1])
                self.ids.data_order_outstanding.ids.box.text = str(data_order_machine[1][2])
                self.ids.data_order_outstanding.ids.mini.text = str(data_order_machine[1][3])
                self.ids.data_order_outstanding.ids.select.text = str(data_order_machine[1][4])
                self.ids.data_order_outstanding.ids.blue.text = str(data_order_machine[1][5])
        else:
            pass
        # Loads data into non-process flowers labels
        DataController.update_begging_state_order_ongoing()
        data_non_process_flower = DataController.check_non_process_flowers()
        self.ids.label_quantity_mini.text = str(data_non_process_flower[0])
        self.ids.label_quantity_select.text = str(data_non_process_flower[1])
        self.ids.label_quantity_blue.text = str(data_non_process_flower[2])


class Order(BoxLayout):
    def create_order(self):
        quantity_mini = self.ids["field_order_quantity_mini"].text
        quantity_select = self.ids["field_order_quantity_select"].text
        quantity_blue = self.ids["field_order_quantity_blue"].text
        box_size = self.ids["field_order_box_size"].text
        order_id = self.ids["field_order_id"].text
        self.check_username(quantity_mini, quantity_select, quantity_blue, box_size, order_id)
        self.parent.parent.parent.parent.parent.parent.parent.parent.ids.home.charge_data()

    def check_username(self, mini, select, blue, box_size, order_id):
        check_data = False
        if not re.match("[pmgPMG]", box_size) or box_size.split() == []:
            check_data = True
        if not re.match(r'\d', mini) or mini.split() == []:
            check_data = True
        if not re.match(r'\d', select) or select.split() == []:
            check_data = True
        if not re.match(r'\d', blue) or blue.split() == []:
            check_data = True
        if not re.match(r'\d', order_id) or order_id.split() == []:
            check_data = True

        if check_data:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Dato Invalido',
                text='Por favor verifique los datos ingresados',
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            notice = DataController.create_order(current_session.get_username(), mini, select, blue, box_size, order_id)
            cancel_btn_username_dialogue = MDFlatButton(
                    text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Aviso',
                text=notice,
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            self.ids["field_order_quantity_mini"].text = ''
            self.ids["field_order_quantity_select"].text = ''
            self.ids["field_order_quantity_blue"].text = ''
            self.ids["field_order_box_size"].text = ''
            self.ids["field_order_id"].text = ''

    def delete_order(self):
        order_id = self.ids["field_order_id"].text
        data_check = False
        if not re.match(r'\d', order_id) or order_id.split() == []:
            data_check = True
        if data_check:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Dato Invalido',
                text='Por favor verifique los datos ingresados',
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            notice = DataController.delete_order(order_id)
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Aviso',
                text=notice,
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            self.ids["field_order_id"].text = ''

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()


class Stats(BoxLayout):
    def on_kv_post(self, base_widget):
        self.calculate_begging_stats()

    def calculate_stats(self):
        begging_date = self.ids.field_stats_date_start.text
        end_date = self.ids.field_stats_date_end.text
        if re.match(r'\d{4}-\d{2}-\d{2}', begging_date) is not None and \
                re.match(r'\d{4}-\d{2}-\d{2}', end_date) is not None:
            data_stats = DataController.calculate_stats(begging_date, end_date)
            self.ids.global_flower_quantity.text = str(data_stats[0]["Total_Flower"])
            self.ids.stats_quantity_select.text = str(data_stats[0]["Total_Select"])
            self.ids.stats_quantity_mini.text = str(data_stats[0]["Total_Mini"])
            self.ids.stats_quantity_blue.text = str(data_stats[0]["Total_Blue"])
            self.ids.performance.text = str(data_stats[0]["Performance"]) + '  flores / min'
            self.ids.global_order_quantity.text = str(data_stats[0]["Total_Order"])
            self.ids.average_ndvi.text = str(data_stats[0]["Noir"])
            self.ids.average_gci.text = str(data_stats[0]["Gci"])
        else:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Cerrar', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Aviso',
                text='Por favor verifique que la fecha en este en formato "aaaa-mm-dd"',
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    def calculate_begging_stats(self):
        data_stats = DataController.calculate_stats()
        self.ids.global_flower_quantity.text = str(data_stats[0]["Total_Flower"])
        self.ids.stats_quantity_select.text = str(data_stats[0]["Total_Select"])
        self.ids.stats_quantity_mini.text = str(data_stats[0]["Total_Mini"])
        self.ids.stats_quantity_blue.text = str(data_stats[0]["Total_Blue"])
        self.ids.performance.text = str(float("{:.2f}".format(data_stats[0]["Performance"])))+ '  flores / min'
        self.ids.global_order_quantity.text = str(data_stats[0]["Total_Order"])
        self.ids.average_ndvi.text = str(float("{:.2f}".format(data_stats[0]["Noir"])))
        self.ids.average_gci.text = str(float("{:.2f}".format(data_stats[0]["Gci"])))


class History(BoxLayout):
    pass


class Setting(BoxLayout):
    pass


class Toolbar(MDToolbar):
    pass


class DataOrderActive(BoxLayout):
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

        if not re.match("^[a-zA-z]", username):
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
                self.parent.parent.parent.parent.ids.content_drawer.ids.name_account.text = current_session.get_username()
                if current_session.get_role() == '1':
                    self.parent.parent.parent.parent.ids.content_drawer.ids.role_account.text = 'Admin'
                else:
                    self.parent.parent.parent.parent.ids.content_drawer.ids.role_account.text = 'Operario'
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


class DataTableOrderActive(AnchorLayout):
    def __init__(self, **kwargs):
        super(DataTableOrderActive, self).__init__()
        data_active_orders = DataController.search_active_orders()
        self.data_tables = MDDataTable(
            size_hint=(0.9, .9),
            rows_num=30,
            id='data_table_order_reload',
            # name column, width column
            column_data=[
                ("#", dp(8)),
                ("Pedido", dp(15)),
                ("Estado", dp(20)),
                ("Posición Caja", dp(15)),
                ("Caja", dp(15)),
                ("Mini", dp(10)),
                ("Selecta", dp(15)),
                ("Azul", dp(15))
            ], row_data=data_active_orders
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.add_widget(self.data_tables)

    def on_row_press(self, instance_table, instance_row):
        data_active_orders = DataController.search_active_orders()
        instance_table.row_data = data_active_orders


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


class DataOrderActiveTitle(BoxLayout):
    pass


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
    label = None

    def build(self):
        self.title = "HydrangeaApp"
        reactor.listenTCP(8000, EchoServerFactory(self))
        self.theme_cls.primary_palette = "Indigo"

    def on_start(self):
        self.root.ids.screen_manager.current = 'Screen Login'

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        print("received:  {}\n".format(msg))
        if msg == "Select" or "Blue" or "Mini":
            data_flower = DataController.check_non_process_flowers()
            if not statistics.mean(data_flower) > 0:
                DataController.update_state_finish_order()
                DataController.update_begging_state_order_ongoing()
                self.root.ids.home.charge_data()
            if msg == "Select":
                print(DataController.update_outstanding_select())
                self.root.ids.home.ids.label_flower_type.text = 'Mini'
            if msg == "Blue":
                print(DataController.update_outstanding_blue())
                self.root.ids.home.ids.label_flower_type.text = 'Blue'
            if msg == 'Mini':
                print(DataController.update_outstanding_mini())
                self.root.ids.home.ids.label_flower_type.text = 'Mini'
            data_flower = DataController.check_non_process_flowers()
            if not statistics.mean(data_flower) > 0:
                DataController.update_state_finish_order()
                DataController.update_begging_state_order_ongoing()
                self.root.ids.home.charge_data()
            data_flower = DataController.check_non_process_flowers()
            self.root.ids.home.ids.label_quantity_mini.text = str(data_flower[0])
            self.root.ids.home.ids.label_quantity_select.text = str(data_flower[1])
            self.root.ids.home.ids.label_quantity_blue.text = str(data_flower[2])

        if msg == 'Start':
            self.root.ids.home.ids.flower_image.source = '/home/agoez/Pictures/anki2.jpg'
            print('On')
        print("responded: {}\n".format(msg))
        return msg.encode('utf-8')


if __name__ == "__main__":
    MainApp().run()
    # Ejes.initConfig()
