# -*-coding utf-8-*-
# install_twisted_rector must be called before importing and using the reactor
import os

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.gridlayout import GridLayout
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
from HydrangeaApp.temp.captureCamera import CaptureImage

import statistics
import re
import json
import sys

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol

sys.path.insert(0, '/home/pi/Documents/TG/hydrangea-app/')


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app

import _thread
# from HydrangeaApp.temp import Ejes
#
# traslX = Ejes.Traslacional(4, 10, 16)
# traslY = Ejes.Traslacional(5, 11, 17)
# traslZ = Ejes.Elevador(6, 12, 18)
# rotY = Ejes.RotacionalPlanterios(8, 13)
# rotX = Ejes.Rotacional(13, 14)
# pinzas = Ejes.Pinzas(11, 15, 19, 20)


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

    def turn_on_machine(self, *args):
        if self.ids.button_on.text == 'OFF':
            self.ids.button_on.text = 'ON'
            # pinzas.turn_on_sensor(True)
        else:
            self.ids.button_on.text = 'OFF'
            # pinzas.turn_on_sensor(False)

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
        # self.ids.global_flower_quantity.text = str(data_stats[0]["Total_Flower"])
        # self.ids.stats_quantity_select.text = str(data_stats[0]["Total_Select"])
        # self.ids.stats_quantity_mini.text = str(data_stats[0]["Total_Mini"])
        # self.ids.stats_quantity_blue.text = str(data_stats[0]["Total_Blue"])
        # self.ids.performance.text = str(float("{:.2f}".format(data_stats[0]["Performance"]))) + 'flores / min'
        # self.ids.global_order_quantity.text = str(data_stats[0]["Total_Order"])
        if data_stats[0]["Noir"] is not None:
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

    def gripper_pressed(self):
        print('gripper_on')
        if self.home == 1:
            if self.parent.ids.btn_on_gripper.text == "ON":
                # _thread.start_new_thread(pinzas.POpen,())
                self.parent.ids.btn_on_gripper.text = "OFF"
            else:
                # _thread.start_new_thread(pinzas.PStop,())
                self.parent.ids.btn_on_gripper.text = "ON"
        else:
            print ("Home primero")

    def gripper_pressed_home(self):
        print('gripper_home')
        # pinzas.PHome()
        self.home = 1

    def rot_x_btn_up(self):
        print('rot_x_up')
        # rotX.ManualUp()
        # self.parent.ids.text_rot_x.text = str(rotX.grados)

    def rot_x_btn_down(self):
        print('rot_x_down')
        # rotX.ManualDown()
        # self.parent.ids.text_rot_x.text = str(rotX.grados)

    def rot_x_btn_goto(self):
        print('rot_x_goto')
        # rotX.ManualDown()
        # GoRotX=int(self.parent.ids.text_rot_x.text)
        # rotX.GotoGrados(GoRotX,80)
        # self.parent.ids.text_rot_x.text = str(rotX.grados)

    def rot_x_btn_reset(self):
        print('rot_x_reset')
        # rotX.ResetHome()
        # self.parent.ids.text_rot_x.text = str(rotX.grados)

    def rot_y_btn_up(self):
        print('rot_y_up')
        # rotY.ManualUp()
        # self.parent.ids.text_rot_y.text = str(rotY.grados)

    def rot_y_btn_down(self):
        print('rot_y_down')
        # rotY.ManualDown()
        # self.parent.ids.text_rot_y.text = str(rotY.grados)

    def rot_y_btn_goto(self):
        print('rot_y_goto')
        # GoRotY=int(self.parent.ids.text_rot_y.text)
        # rotY.GotoGrados(GoRotY,80)
        # self.parent.ids.text_rot_y.text) = str(rotY.grados)

    def rot_y_btn_reset(self):
        print('rot y reset')
        # rotY.ResetHome()
        # self.parent.ids.text_rot_y.text = str(rotY.grados)

    def btn_x_up(self):
        print('x up')
        # traslX.ManualUp()
        # self.parent.ids.text_axis_x.text = str(traslX.distancia)

    def btn_x_down(self):
        print('x down')
        # traslX.ManualDown()
        # self.parent.ids.text_axis_x.text = str(traslX.distancia)

    def btn_x_goto(self):
        print('x goto')
        # GoX=int(self.parent.ids.text_axis_x.text)
        # traslX.GotoDistancia(GoX,300)
        # self.parent.ids.text_axis_x.text = str(traslX.distancia)

    def btn_x_reset(self):
        print('x reset')
        # traslX.ResetHome()
        # self.parent.ids.text_axis_x.text = str(traslX.distancia)

    def btn_y_up(self):
        print('y up')
        # traslY.ManualUp()
        # self.parent.ids.text_axis_y.text = str(traslY.distancia)

    def btn_y_down(self):
        print('y down')
        # traslY.ManualDown()
        # self.parent.ids.text_axis_y.text = str(traslY.distancia)

    def btn_y_goto(self):
        print('y goto')
        # GoY=int(self.parent.ids.text_axis_y.text)
        # traslY.GotoDistancia(GoY,300)
        # self.parent.ids.text_axis_y.text = str(traslY.distancia)

    def btn_y_reset(self):
        print('y reset')
        # traslY.ResetHome()
        # self.parent.ids.text_axis_y.text = str(traslY.distancia)

    def btn_z_up(self):
        print('z up')
        # traslZ.ManualUp()
        # self.parent.ids.text_axis_z.text = str(traslZ.distancia)

    def btn_z_down(self):
        print('z down')
        # traslZ.ManualDown()
        # self.parent.ids.text_axis_z.text = str(traslZ.distancia)

    def btn_z_goto(self):
        print('z goto')
        # GoZ=int(self.parent.ids.text_axis_z.text)
        # traslZ.GotoDistancia(GoZ,1000)
        # self.parent.ids.text_axis_z.text = str(traslZ.distancia)

    def btn_z_reset(self):
        print('z reset')
        # traslZ.ResetHome()
        # self.parent.ids.text_axis_z.text = str(traslZ.distancia)


class DataOrderActiveTitle(BoxLayout):
    pass


class MainApp(MDApp):
    label = None

    def build(self):
        self.title = "HydrangeaApp"
        reactor.listenTCP(8200, EchoServerFactory(self))
        self.theme_cls.primary_palette = "Indigo"

    def on_start(self):
        self.root.ids.screen_manager.current = 'Screen Login'

    def handle_message(self, msg):
        request = json.loads(msg)
        msg = request['type']
        print("received:  {}\n".format(msg))
        if msg == "Select" or "Blue" or "Mini":
            data_flower = DataController.check_non_process_flowers()
            if not statistics.mean(data_flower) > 0:
                DataController.update_state_finish_order()
                DataController.update_begging_state_order_ongoing()
                self.root.ids.home.charge_data()
            if msg == "Select":
                if DataController.update_outstanding_select() is None:
                    self.root.ids.home.ids.label_flower_type.text = 'Mini'
                    # traslX = Ejes.Traslacional(4, 10, 16)
                else:
                    self.root.ids.home.ids.label_flower_type.text = 'No corresponde a pedido'
            if msg == "Blue":
                if DataController.update_outstanding_blue() is None:
                    self.root.ids.home.ids.label_flower_type.text = 'Blue'
                    # traslX = Ejes.Traslacional(4, 10, 16)
                else:
                    self.root.ids.home.ids.label_flower_type.text = 'No corresponde a pedido'
                    # traslX = Ejes.Traslacional(4, 10, 16)
            if msg == 'Mini':
                if DataController.update_outstanding_mini() is None:
                    self.root.ids.home.ids.label_flower_type.text = 'Mini'
                else:
                    self.root.ids.home.ids.label_flower_type.text = 'No corresponde a pedido'
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
            order = self.root.ids.home.ids.data_order_ongoing.ids.order_id.text
            select = int(self.root.ids.home.ids.data_order_ongoing.ids.select.text)
            mini = int(self.root.ids.home.ids.data_order_ongoing.ids.mini.text)
            blue = int(self.root.ids.home.ids.data_order_ongoing.ids.blue.text)
            total = select + mini + blue
            folder_images = '/home/agoez/Pictures/'
            path_image = folder_images + order + '-' + 'rgb' + str(total)
            # CaptureImage.main(path_image)
            self.root.ids.home.ids.flower_image.source = path_image
        if msg == 'noir':
            print('NOIR')
            print('On')
        print("responded: {}\n".format(msg))
        return msg.encode('utf-8')


if __name__ == "__main__":
    MainApp().run()
    # Ejes.initConfig()