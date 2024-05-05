import random

import allure
import requests

from urls import Address


class UserCreationHelper:
    @staticmethod
    @allure.step('Создание учетной записи пользователя')
    def user_creation_request(data):
        response = requests.post(f"{Address.url}{Address.create_user}", data=data)
        return response


class UserDeletionHelper:
    @staticmethod
    @allure.step('Удаление учетной записи пользователя')
    def user_deletion_requests(token):
        response = requests.delete(f'{Address.url}{Address.delete_user}', headers={"Authorization": token})
        return response


class UserAuthorizationHelper:
    @staticmethod
    @allure.step('Авторизация пользователя')
    def user_authorization_requests(email, password):
        response = requests.post(f'{Address.url}{Address.auth_user}', data={"email": email, "password": password})
        return response


class UserChangeDataHelper:
    @staticmethod
    @allure.step('Изменение данных пользователя')
    def user_change_data_requests(email, password, name, token):
        response = requests.patch(f'{Address.url}{Address.change_data}',
                                  data={"email": email, "password": password, "name": name},
                                  headers={"Authorization": token})
        return response


class GetIngredientsHelper:
    @staticmethod
    @allure.step('Получить список случайных ингредиентов')
    def get_random_ingredients_requests():
        response = requests.get('https://stellarburgers.nomoreparties.site/api/ingredients')
        ingredients = [i['_id'] for i in response.json()['data']]
        return [random.choice(ingredients) for _ in range(random.randint(1, 4))]


class CreatingAnOrderHelper:
    @staticmethod
    @allure.step('Создание заказа')
    def creating_an_order_requests(ingredients, token=""):
        response = requests.post(f'{Address.url}{Address.create_order}',
                                 data={"ingredients": ingredients},
                                 headers={"Authorization": token})
        return response


class ReceivingOrdersHelper:
    @staticmethod
    @allure.step('Получение заказов пользователя')
    def receiving_orders_requests(token=""):
        response = requests.get(f'{Address.url}{Address.get_user_orders}', headers={"Authorization": token})
        return response
