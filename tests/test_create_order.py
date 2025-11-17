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
        payload = {'ingredients': generators.generate_list_ingredients(1, get_ingredients)}
        with allure.step('Создание заказа без авторизации'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_CREATE_ORDER}', json=payload)
        assert response.status_code == 200, f'Ожидали 200 без авторизации, получили {response.status_code}'
        assert response.json().get('success') is True

    @pytest.mark.parametrize('hash_ingredient', data.Ingredients.INVALID_HASH)
    @allure.title('Тест создания заказа с невалидным хэшом ингредиента')
    def test_create_order_with_invalid_hash(self, login_user, hash_ingredient):
        headers = _bearer(login_user['accessToken'])
        payload = {'ingredients': hash_ingredient}
        with allure.step('Создание заказа с невалидным хэшом ингредиента'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_CREATE_ORDER}', json=payload, headers=headers)
        assert response.status_code in (400, 403, 500), f'Ожидали 400/403/500, получили {response.status_code}'

    @allure.title('Тест создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self, login_user):
        headers = _bearer(login_user['accessToken'])
        payload = {'ingredients': []}
        with allure.step('Создание заказа без ингредиентов'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_CREATE_ORDER}', json=payload, headers=headers)
        assert response.status_code == 400, f'Ожидали 400, получили {response.status_code}'
        assert response.json().get('message') == data.ResponseData.RESPONSE_INVALID_CREATE_ORDER['message']


