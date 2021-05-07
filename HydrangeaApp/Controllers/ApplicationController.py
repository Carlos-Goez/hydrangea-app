
from HydrangeaApp.Models.ApplicationModel import DBModel
from HydrangeaApp.Controllers.Encryption import EncryptionPassword


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
