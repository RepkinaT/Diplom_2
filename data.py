import random
from random import randint, choice


class Data:

    @staticmethod
    def get_random_email():
        return f"my_email_{choice(['x', 'y', 'z'])}{randint(1, 10000)}@gmail.com"

    @staticmethod
    def get_random_password():
        return choice(["Pass.1", "Pass.2", "Pass.3"])

    @staticmethod
    def get_random_name():
        return choice(["Name_1", "Name_2", "Name_3"])

    @staticmethod
    def get_random_str():
        return str(random.randint(1, 10000))
