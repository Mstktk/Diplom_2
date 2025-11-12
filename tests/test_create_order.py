import allure
import pytest
import requests
import generators
import data
from curls import Curls

def _bearer(token: str) -> dict:
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]
    return {'Authorization': f'Bearer {token}'}

class TestCreateOrder:
    @allure.title('Тест создания заказа с авторизацией')
    @pytest.mark.parametrize('size', [1, 3, 5])
    def test_create_order_with_authorization(self, login_user, get_ingredients, size):
        headers = _bearer(login_user['accessToken'])
        payload = {'ingredients': generators.generate_list_ingredients(size, get_ingredients)}
        with allure.step(f'Создание заказа с {size} ингредиентами'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_CREATE_ORDER}', json=payload, headers=headers)
        assert response.status_code == 200, f'Ожидали 200, получили {response.status_code}'
        assert response.json().get('success') is True

    @allure.title('Тест создания заказа без авторизации')
    def test_create_order_without_authorization(self, get_ingredients):
        payload
