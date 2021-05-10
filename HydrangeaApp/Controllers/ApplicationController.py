
from HydrangeaApp.Models.ApplicationModel import DBModel
from HydrangeaApp.Controllers.Encryption import EncryptionPassword
from datetime import datetime, timedelta


class DataController:

    @staticmethod
    def singup(username, password, role):
        if DBModel.check_username(username)[0]["Status"]:
            return "El usuario ya esta en uso"
        else:
            hash_pass = EncryptionPassword.encryption(password.encode('utf-8'))
            DBModel.create_user(username, role, hash_pass.decode("utf-8"))
            return "El usuario su creado con éxito"

    @staticmethod
    def login(username, password, session):
        if DBModel.check_username(username)[0]["Status"]:
            user_data = DBModel.login(username)
            if EncryptionPassword.check_password(password.encode('utf-8'), user_data[0]["Password"].encode('utf-8')):
                session.set_role(user_data[0]["Role_ID"])
                session.set_username(user_data[0]["Username"])
                return 1
            else:
                return 0
        else:
            return 0

    @staticmethod
    def create_order(username, quantity_mini, quantity_select, quantity_blue, box_size_arg, order_id):
        mini = int(quantity_mini)
        select = int(quantity_select)
        blue = int(quantity_blue)
        box_size = box_size_arg.capitalize()
        if DBModel.check_order(order_id)[0]["Status"]:
            return 'Ya exista un Pedido con el identificador ingresado'
        elif (box_size == 'P' and (mini + select + blue) > 24) or \
                (box_size == 'M' and (mini + select + blue) > 48) or \
                (box_size == 'G' and (mini + select + blue) > 60):
            return 'La cantidad de flores asignada supera la capacidad de la caja seleccionada.'
        else:
            if DBModel.create_order(order_id, username, mini, select, blue, box_size) == 1:
                return 'Pedido creado con éxito'
            else:
                return 'Algo salio mal reintente en momento'

    @staticmethod
    def delete_order(order_id):
        if not DBModel.check_order_ongoing(order_id)[0]["Status"]:
            return f'No existe un pedido con el identificador "{order_id}" que pueda ser eliminado.'
        else:
            if DBModel.delete_order(order_id):
                return f'El pedido {order_id} se a eliminado con éxito'
            else:
                return 'Algo a salido mal por favor vuelva a intentarlo'

    @staticmethod
    def search_active_orders():
        data_table = DBModel.check_active_orders()
        data_result = []
        for i, row in enumerate(data_table):
            data_result.append((i + 1,
                                data_table[i]["Order_ID"],
                                data_table[i]["Order_Status"],
                                data_table[i]["Packing_Position"],
                                data_table[i]["Size_Box"],
                                data_table[i]["Quantity_Mini"],
                                data_table[i]["Quantity_Select"],
                                data_table[i]["Quantity_Blue"])
                               )
        return data_result

    @staticmethod
    def search_orders_inside_machine():
        data_table = DBModel.search_order_inside_machine()
        data_result = []
        for i, row in enumerate(data_table):
            data_result.append((data_table[i]["Order_ID"],
                                data_table[i]["Packing_Position"],
                                data_table[i]["Size_Box"],
                                data_table[i]["Quantity_Mini"],
                                data_table[i]["Quantity_Select"],
                                data_table[i]["Quantity_Blue"])
                               )
        return data_result

    @staticmethod
    def check_non_process_flowers():
        data_outstanding = DBModel.check_outstanding()
        if len(data_outstanding) == 0:
            return [0, 0, 0]
        else:
            data_result = [data_outstanding[0]["Outstanding_Mini"],
                           data_outstanding[0]["Outstanding_Select"],
                           data_outstanding[0]["Outstanding_Blue"]]
        return data_result

    @staticmethod
    def update_next_active_order():
        if DBModel.update_status_order_ongoing() == 1:
            return 1
        else:
            return 0

    @staticmethod
    def calculate_stats(begging_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                        end_date=(datetime.now().strftime('%Y-%m-%d'))):
        data = DBModel.calculate_stats(begging_date, end_date)
        return data

    @staticmethod
    def update_begging_state_order_ongoing():
        if int(DBModel.check_order_ongoing_begging()[0]["Status"]) == 0:
            DBModel.update_status_order_ongoing()

    @staticmethod
    def update_state_finish_order():
        DBModel.update_order_status_finished()

    @staticmethod
    def update_outstanding_mini():
        if int(DBModel.check_outstanding()[0]["Outstanding_Mini"]) > 0:
            DBModel.update_outstanding_mini()
        else:
            return "La flor Ingresada no corresponde al pedido actual"

    @staticmethod
    def update_outstanding_select():
        if int(DBModel.check_outstanding()[0]["Outstanding_Select"]) > 0:
            DBModel.update_outstanding_select()
        else:
            return "La flor Ingresada no corresponde al pedido actual"

    @staticmethod
    def update_outstanding_blue():
        if int(DBModel.check_outstanding()[0]["Outstanding_Blue"]) > 0:
            DBModel.update_outstanding_blue()
        else:
            return "La flor Ingresada no corresponde al pedido actual"
