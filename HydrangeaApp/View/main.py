# -*-coding utf-8-*-

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable


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


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class DataTable(MDDataTable):
    def __init__(self, **kwargs):
        super(DataTable, self).__init__()
        self.data_tables = MDDataTable(
            orientation='lr-tb',
            size_hint=(0.9, 0.6),
            # name column, width column
            column_data=[
                ("Column 1", dp(30)),
                ("Column 2", dp(30)),
                ("Column 3", dp(30)),
                ("Column 4", dp(30)),
                ("Column 5", dp(30)),
                ("Column 6", dp(30)),
            ],
        )

    def on_start(self):
        self.data_tables.open()


class MainApp(MDApp):
    def build(self):
        self.title = "HydrangeaApp"
        self.theme_cls.primary_palette = "Indigo"
        data_table = DataTable()
        return data_table


MainApp().run()
