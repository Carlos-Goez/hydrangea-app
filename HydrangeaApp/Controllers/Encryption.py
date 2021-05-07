import bcrypt


class EncryptionPassword:

    @staticmethod
    def encryption(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed

    @staticmethod
    def check_password(password, hashed):
        if bcrypt.checkpw(password, hashed):
            return 1
        else:
            return 0
