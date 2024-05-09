import allure

from helpers import CreatingAnOrderHelper, GetIngredientsHelper, ReceivingOrdersHelper


class TestOrder:
    @allure.title('Тест создания заказа с авторизацией с ингредиентами')
    @allure.description("Должны получить в ответе код: 200 и значение 'success': True")
    def test_create_order_with_authorization_with_ingredients(self, create_user_get_data_and_delete_user):
        response = create_user_get_data_and_delete_user[0]
        token = response.json()['accessToken']
        response = CreatingAnOrderHelper.creating_an_order_requests(
            ingredients=GetIngredientsHelper.get_random_ingredients_requests(), token=token)
        assert response.status_code == 200 and response.json().get('success') is True

    @allure.title('Тест создания заказа с авторизацией без ингредиентов')
    @allure.description("Должны получить в ответе код: 400 и значение 'success': False")
    def test_create_order_with_authorization_without_ingredients(self, create_user_get_data_and_delete_user):
        response = create_user_get_data_and_delete_user[0]
        token = response.json()['accessToken']
        response = CreatingAnOrderHelper.creating_an_order_requests(
            ingredients=[], token=token)
        assert response.status_code == 400 and response.json().get('success') is False

    @allure.title('Тест создания заказа с авторизацией с некорректными хешами ингредиентов')
    @allure.description("Должны получить в ответе код: 500")
    def test_create_order_with_authorization_with_incorrect_hash(self, create_user_get_data_and_delete_user):
        response = create_user_get_data_and_delete_user[0]
        token = response.json()['accessToken']
        ingredients = [i + 'bad' for i in GetIngredientsHelper.get_random_ingredients_requests()]
        response = CreatingAnOrderHelper.creating_an_order_requests(ingredients=ingredients, token=token)
        assert response.status_code == 500

    @allure.title('Тест создания заказа без авторизации с ингредиентами')
    @allure.description("Должны получить в ответе код: 200 и значение 'success': True")
    def test_create_order_without_authorization_with_ingredients(self, create_user_get_data_and_delete_user):
        response = CreatingAnOrderHelper.creating_an_order_requests(
            ingredients=GetIngredientsHelper.get_random_ingredients_requests())
        assert response.status_code == 200 and response.json().get('success') is True

    @allure.title('Тест создания заказа без авторизации без ингредиентов')
    @allure.description("Должны получить в ответе код: 400 и значение 'success': False")
    def test_create_order_without_authorization_and_ingredients(self):
        response = CreatingAnOrderHelper.creating_an_order_requests(ingredients=[])
        assert response.status_code == 400 and response.json().get('success') is False

    @allure.title('Тест создания заказа без авторизации с некорректными хешами ингредиентов')
    @allure.description("Должны получить в ответе код: 500")
    def test_create_order_without_authorization_with_incorrect_hash(self):
        ingredients = [i + 'bad' for i in GetIngredientsHelper.get_random_ingredients_requests()]
        response = CreatingAnOrderHelper.creating_an_order_requests(ingredients=ingredients)
        assert response.status_code == 500

    @allure.title('Тест получения списка заказов авторизованного пользователя')
    @allure.description("Должны получить в ответе код: 200 и значение 'success': True")
    def test_receiving_orders_from_an_authorized_user(self, create_user_get_data_and_delete_user):
        response = create_user_get_data_and_delete_user[0]
        token = response.json()['accessToken']
        CreatingAnOrderHelper.creating_an_order_requests(
            ingredients=GetIngredientsHelper.get_random_ingredients_requests(), token=token)
        response = ReceivingOrdersHelper.receiving_orders_requests(token)
        assert response.status_code == 200 and response.json().get('success') is True

    @allure.title('Тест получения списка заказов неавторизованного пользователя')
    @allure.description("Должны получить в ответе код: 200 и значение 'success': True")
    def test_receiving_orders_from_an_authorized_user(self, create_user_get_data_and_delete_user):
        response = ReceivingOrdersHelper.receiving_orders_requests()
        assert response.status_code == 401 and response.json().get('success') is False
