# -*-coding utf-8-*-

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock


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
    pass


class SignUp(BoxLayout):
    pass


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


class MainApp(MDApp):
    def build(self):
        self.title = "HydrangeaApp"
        self.theme_cls.primary_palette = "Indigo"

    def on_start(self):
        self.root.ids.screen_manager.current = 'Screen Login'


MainApp().run()
