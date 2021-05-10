import sqlite3


class DBModel:

    db_path = '../Models/database.db'

    @staticmethod
    def print_hello():
        print("hello!!!!!")

    @staticmethod
    def dict_factory(cursor, row):
        data_dict = {}
        for idx, col in enumerate(cursor.description):
            data_dict[col[0]] = row[idx]
        return data_dict

    @staticmethod
    def create_user(user, role, password):
        db = sqlite3.connect(DBModel.db_path)
        query_beginning = 'INSERT INTO User (Username, Role_ID, Password)'
        query_end = f'VALUES ("{user}", {role}, "{password}" )'
        try:
            cursor = db.cursor()
            cursor.execute(query_beginning + ' ' + query_end)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def check_username(user):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f'SELECT COUNT(*) AS Status FROM User WHERE Username = "{user}"'
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data

    @staticmethod
    def login(user):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f'SELECT * FROM User WHERE Username = "{user}"'
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_user = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_user

    @staticmethod
    def check_order(order_id):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f'SELECT COUNT(*) AS Status FROM OrderHistory WHERE Order_ID = {order_id}'
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data

    @staticmethod
    def search_order_inside_machine():
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f'SELECT * FROM OrderHistory ' \
                f'WHERE (Order_Status = "En Proceso" OR Order_Status = "Pendiente") ORDER BY Creation_Date LIMIT 2'
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data

    @staticmethod
    def check_order_ongoing(order_id):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f'SELECT COUNT(*) AS Status FROM OrderHistory WHERE Order_ID = {order_id} ' \
                f'AND (Order_Status = "En Proceso" OR Order_Status = "Pendiente")'
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data

    @staticmethod
    def create_order(order_id, username, quantity_mini, quantity_select, quantity_blue, size_box):
        db = sqlite3.connect(DBModel.db_path)
        query_beginning = """INSERT INTO OrderHistory (Order_ID,
                           Order_Status,
                           Username,
                           Creation_Date,
                           Quantity_Mini,
                           Quantity_Select,
                           Quantity_Blue,
                           Outstanding_Mini,
                           Outstanding_Select,
                           Outstanding_Blue,
                           Packing_Position,
                           Size_Box) """
        query_end = f"""VALUES ( {order_id}, 'Pendiente', '{username}',
                           (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now'))),
                           {quantity_mini},
                           {quantity_select},
                           {quantity_blue},
                           {quantity_mini},
                           {quantity_select},
                           {quantity_blue},
                           (CASE
                               WHEN (SELECT Packing_Position FROM OrderHistory ORDER BY ROWID DESC LIMIT 1) < 2 
                                    THEN (SELECT Packing_Position FROM OrderHistory ORDER BY ROWID DESC LIMIT 1) + 1
                               ELSE 1
                            END
                               ),
                           '{size_box}') """
        try:
            cursor = db.cursor()
            cursor.execute(query_beginning + " " + query_end)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def delete_order(order_id):
        db = sqlite3.connect(DBModel.db_path)
        query = f"DELETE FROM OrderHistory WHERE Order_ID = {order_id}"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def check_active_orders():
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = "SELECT * FROM OrderHistory " \
                "WHERE Order_Status = 'Pendiente' or  Order_Status = 'En Proceso' " \
                "ORDER BY Creation_Date"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_order_active = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_order_active

    @staticmethod
    def check_orders():
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = "SELECT * FROM OrderHistory"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_order = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_order

    @staticmethod
    def check_order_ongoing_begging():
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f"SELECT COUNT(*) AS Status FROM OrderHistory WHERE Order_Status = 'En Proceso'"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_order = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_order

    @staticmethod
    def update_status_order_ongoing():
        db = sqlite3.connect(DBModel.db_path)
        query = """UPDATE OrderHistory
                        SET Production_Date = (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now'))),
                            Order_Status = 'En Proceso'
                        WHERE Order_Status = 'Pendiente' 
                                AND Creation_Date = (SELECT Creation_Date FROM OrderHistory 
                                                        WHERE Order_Status = 'Pendiente' 
                                                        ORDER BY Creation_Date LIMIT 1);"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def update_order_status_finished():
        db = sqlite3.connect(DBModel.db_path)
        query = f"""UPDATE OrderHistory
                        SET Finish_Date = (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now'))),
                            Order_Status = 'Finalizado'
                        WHERE Order_Status = 'En Proceso'"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def check_outstanding():
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = "SELECT Outstanding_Select, Outstanding_Blue, Outstanding_Mini " \
                "FROM OrderHistory WHERE Order_Status = 'En Proceso'"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_outstanding = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_outstanding

    @staticmethod
    def update_outstanding_mini():
        db = sqlite3.connect(DBModel.db_path)
        query = """UPDATE OrderHistory
                        SET Outstanding_Mini= Outstanding_Mini - 1
                        WHERE Order_Status = 'En Proceso'"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def update_outstanding_blue():
        db = sqlite3.connect(DBModel.db_path)
        query = """UPDATE OrderHistory
                            SET Outstanding_Blue = Outstanding_Blue - 1
                            WHERE Order_Status = 'En Proceso'"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def update_outstanding_select():
        db = sqlite3.connect(DBModel.db_path)
        query = """UPDATE OrderHistory
                            SET Outstanding_Select = Outstanding_Select - 1
                            WHERE Order_Status = 'En Proceso'"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def insert_image(order_id, image_rgb, image_noir, flower_type, ndvi, gci):
        db = sqlite3.connect(DBModel.db_path)
        query = f""" INSERT INTO ImageHistory (Order_ID,
                           File_Path_RGB,
                           File_Path_NOIR,
                           Flower_Type,
                           NOIR,
                           GCI,
                           Capture_Date)
                           VALUES (
                                   {order_id},
                                   '{image_rgb}',
                                   '{image_noir}',
                                   '{flower_type}',
                                    {ndvi},
                                    {gci},
                                    (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now')))
                                  )"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
        except Exception as e:
            return e
        return 1

    @staticmethod
    def history_images(order_id):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f"SELECT * FROM ImageHistory WHERE Order_ID = {order_id}"
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_images_history = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_images_history

    @staticmethod
    def calculate_stats(begging_date, end_date):
        db = sqlite3.connect(DBModel.db_path)
        db.row_factory = DBModel.dict_factory
        query = f"""SELECT  AVG(NOIR) AS Noir,
                            AVG(GCI) AS Gci,  
                            COUNT(DISTINCT Order_ID) AS Total_Order, 
                            COUNT(DISTINCT Image_ID) AS Total_Flower,
                            (SELECT COUNT(*) 
                                FROM ImageHistory 
                                WHERE Flower_Type = 'Mini' AND Capture_Date 
                                    BETWEEN DATE ('{begging_date}') AND DATE ('{end_date}', + '+1 day')) AS Total_Mini,
                            (SELECT COUNT(*) 
                                FROM ImageHistory 
                                WHERE Flower_Type = 'Selecta' AND Capture_Date 
                                    BETWEEN DATE ('{begging_date}') AND DATE ('{end_date}', '+1 day')) AS Total_Select,
                            (SELECT COUNT(*) 
                                FROM ImageHistory 
                                WHERE Flower_Type = 'Blue' AND Capture_Date 
                                    BETWEEN DATE ('{begging_date}') AND DATE ('{end_date}', '+1 day')) AS Total_Blue,
                            (SELECT AVG((julianday(Finish_Date) - julianday(Production_Date))*24*60/(Quantity_Blue + 
                                                                                                     Quantity_Mini + 
                                                                                                     Quantity_Select))
                              FROM OrderHistory 
                              WHERE Finish_Date 
                                BETWEEN DATE ('{begging_date}') AND DATE ('{end_date}', '+1 day')) AS Performance
                        FROM ImageHistory 
                        WHERE Capture_Date 
                            BETWEEN DATE ('{begging_date}') AND DATE ('{end_date}', '+1 day')"""
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data_stats = cursor.fetchall()
            db.commit()
            db.close()
        except Exception as e:
            return e
        return data_stats
