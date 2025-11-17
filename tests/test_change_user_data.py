import pytest
import requests
import data
import allure
import generators
from curls import Curls

def _bearer(token: str) -> dict:
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]
    return {'Authorization': f'Bearer {token}'}

class TestChangeUserData:
    @allure.title('Тест изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('change_param, generate_method', [['email', 'generate_email'], ['name', 'generate_name']])
    def test_change_user_data_with_login(self, login_and_return_data, change_param, generate_method):
        access_token = login_and_return_data['accessToken']
        generate_param = getattr(generators, generate_method)
        payload = {change_param: generate_param()}
        with allure.step(f'Изменение {change_param} пользователя'):
            response = requests.patch(
                f'{Curls.MAIN_URL}{Curls.URL_CHANGE_USER_DATA}',
                json=payload,
                headers=_bearer(access_token)
            )
        assert response.status_code == 200
        body = response.json()
        assert body.get('success') is True
        assert body.get('user', {}).get(change_param) == payload[change_param]

    @allure.title('Тест изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('change_param, generate_method', [['email', 'generate_email'], ['name', 'generate_name']])
    def test_change_user_data_without(self, change_param, generate_method):
        generate_param = getattr(generators, generate_method)
        payload = {change_param: generate_param()}
        with allure.step(f'Изменение {change_param} пользователя без авторизации'):
            response = requests.patch(f'{Curls.MAIN_URL}{Curls.URL_CHANGE_USER_DATA}', json=payload)
        assert response.status_code == 401
        assert response.json().get('message') == data.ResponseData.RESPONSE_ERROR_CHANGE_USER_DATA['message']

    @allure.title('Тест изменения почты пользователя на уже используемую')
    def test_change_user_email(self, login_and_return_data):
        access_token = login_and_return_data['accessToken']
        payload = {'email': data.UserData.USER_EMAIL}
        with allure.step('Изменение почты пользователя на уже используемую'):
            response = requests.patch(
                f'{Curls.MAIN_URL}{Curls.URL_CHANGE_USER_DATA}',
                json=payload,
                headers=_bearer(access_token)
            )
        assert response.status_code == 403, f'Ожидали 403, получили {response.status_code}'
        assert response.json().get('message') == data.ResponseData.RESPONSE_ERROR_CHANGE_EMAIL['message']

