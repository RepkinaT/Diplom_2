import allure
import pytest

from data import Data
from helpers import UserCreationHelper, UserAuthorizationHelper, UserChangeDataHelper


class TestUser:
    @allure.title('Тест создания пользователя')
    @allure.description("Создаем запись пользователя передавая email, пароль и имя. "
                        "Должны получить в ответе код: 200 и значение 'success': True")
    def test_create_user_successful(self, create_user_get_data_and_delete_user):
        response = create_user_get_data_and_delete_user[0]
        token = response.json().get("accessToken")
        assert response.status_code == 200 and token.startswith("Bearer")

    @allure.title('Тест невозможности создания дубликата учетной записи пользователя')
    @allure.description("Создаем запись пользователя передавая email, пароль и имя, затем пытаемся создать еще запись "
                        "с тем же email. Должны получить в ответе код: "
                        "403 и значение 'success': False")
    def test_create_user_already_exists(self, create_user_get_data_and_delete_user):
        response, account_details = create_user_get_data_and_delete_user
        response = UserCreationHelper.user_creation_request(
            {"email": response.json().get('user').get('email'), "password": account_details.get('password'),
             "name": account_details.get('name')})
        message = response.json().get('message')
        assert response.status_code == 403 and message == "User already exists"

    @pytest.mark.parametrize('missing_data', ('email', 'password', 'name'))
    @allure.title('Тест невозможности создания пользователя с незаполненным обязательным полем')
    @allure.description("Создаем запись пользователя заполняя не все обязательные поля "
                        "Должны получить в ответе код: 403 и значение 'success': False")
    def test_create_user_without_required_data(self, get_the_user_data, missing_data):
        del get_the_user_data[missing_data]
        response = UserCreationHelper.user_creation_request(missing_data)
        message = response.json().get('message')
        assert response.status_code == 403 and message == "Email, password and name are required fields"

    @allure.title('Тест авторизации пользователя')
    @allure.description("Создаем запись пользователя передавая email, пароль и имя. "
                        "Затем входим с созданным логином и паролем."
                        "Должны получить в ответе код: 200 и значение 'success': True")
    def test_user_authorization_successful(self, create_user_get_data_and_delete_user):
        response, account_details = create_user_get_data_and_delete_user
        response = UserAuthorizationHelper.user_authorization_requests(account_details.get('email'),
                                                                       account_details.get('password'))
        assert response.status_code == 200 and response.json().get('success') is True

    @pytest.mark.parametrize('data_change', ('email', 'password'))
    @allure.title('Тест невозможности авторизации пользователя с неверными данными')
    @allure.description("Создаем запись пользователя передавая email, пароль и имя. "
                        "Затем входим с заведомо неверными логином и паролем."
                        "Должны получить в ответе код: 401 и значение 'success': False")
    def test_user_authorization_with_incorrect_data(
            self, create_user_get_data_and_delete_user, data_change):
        response, account_details = create_user_get_data_and_delete_user
        account_details[data_change] = Data.get_random_str() + account_details.get(data_change)
        response = UserAuthorizationHelper.user_authorization_requests(account_details.get('email'),
                                                                       account_details.get('password'))
        message = response.json().get('message')
        assert response.status_code == 401 and message == 'email or password are incorrect'

    @pytest.mark.parametrize('data_change', ('email', 'password', 'name'))
    @allure.title('Тест изменения данных пользователя с авторизацией')
    @allure.description("Должны получить в ответе код: 200 и значение 'success': True")
    def test_change_data_authorization_user(self, create_user_get_data_and_delete_user, data_change):
        response, account_details = create_user_get_data_and_delete_user
        response = UserAuthorizationHelper.user_authorization_requests(account_details.get('email'),
                                                                       account_details.get('password'))
        token = response.json()['accessToken']
        account_details[data_change] = Data.get_random_str() + account_details.get(data_change)
        UserChangeDataHelper.user_change_data_requests(account_details.get('email'), account_details.get('password'),
                                                       account_details.get('name'), token)
        assert response.status_code == 200 and response.json().get('success') is True

    @pytest.mark.parametrize('data_change', ('email', 'password', 'name'))
    @allure.title('Тест изменения данных пользователя без авторизации')
    @allure.description("Должны получить в ответе код: 401 и значение 'message': You should be authorised")
    def test_change_data_not_authorization_user(self, create_user_get_data_and_delete_user, data_change):
        response, account_details = create_user_get_data_and_delete_user
        token = ''
        account_details[data_change] = Data.get_random_str() + account_details.get(data_change)
        response = UserChangeDataHelper.user_change_data_requests(account_details.get('email'),
                                                                  account_details.get('password'),
                                                                  account_details.get('name'), token)
        message = response.json().get('message')
        assert response.status_code == 401 and message == "You should be authorised"
