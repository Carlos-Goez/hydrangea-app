import json


class Auth:
    __data = {}

    def create_session(self, user, role):
        self.__data = {'user': user, 'role': role, 'is_logged': True}

        with open('data.json', 'w') as file:
            json.dump(self.__data, file, indent=4)

    @staticmethod
    def see_session():
        with open('data.json', 'r') as file:
            data = json.load(file)
            return data

    @staticmethod
    def logout():
        data = {'user': '', 'role': '', 'is_logged': False}
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.truncate()

