import allure
import requests
import data
from curls import Curls
from helpers import _bearer

class TestGetOrder:
    @allure.title('Тест получения заказов пользователя с авторизацией')
    def test_get_order_with_authorization(self, login_user):
        headers = _bearer(login_user['accessToken'])
        with allure.step('Получение заказов пользователя'):
            response = requests.get(f'{Curls.MAIN_URL}{Curls.URL_GET_USER_ORDERS}', headers=headers)
        assert response.status_code == 200
        assert response.json().get('success') is True

    @allure.title('Тест получения заказов пользователя без авторизации')
    def test_get_order_without_authorization(self):
        with allure.step('Получение заказов пользователя'):
            response = requests.get(f'{Curls.MAIN_URL}{Curls.URL_GET_USER_ORDERS}')
        assert response.status_code == 401
        assert response.json().get('message') == data.ResponseData.RESPONSE_ERROR_GET_ORDERS['message']

