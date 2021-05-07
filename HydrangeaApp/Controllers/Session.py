class Session:
    def __init__(self, username=None, role=None):
        self.__username = username
        self.__role = role

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_role(self):
        return self.__role

    def set_role(self, role):
        self.__role = role
