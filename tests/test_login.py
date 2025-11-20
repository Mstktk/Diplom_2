import allure
import requests
import pytest
import data
import generators
from curls import Curls

class TestLogin:
    @allure.title('Тест авторизации пользователя')
    def test_login_user(self):
        payload = {'email': data.UserData.USER_EMAIL, 'password': data.UserData.USER_PASSWORD}
        with allure.step('Авторизация пользователя'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload) 
        assert response.status_code == 200, f'Ожидали 200, получили {response.status_code}'
        body = response.json()
        assert body.get('success') is True
        assert body.get('user', {}).get('email') == data.UserData.USER_EMAIL
        assert body.get('user', {}).get('name') == data.UserData.USER_NAME

    @allure.title('Тест авторизации с неверным паролем')
    def test_login_invalid_password(self):
        payload = {
            'email': data.UserData.USER_EMAIL,
            'password': generators.generate_password()
        }
        with allure.step('Авторизация с неверным паролем'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload)  
        assert response.status_code == 401
        assert response.json().get('message') == data.ResponseData.RESPONSE_INVALID_LOGIN['message']

    @allure.title('Тест авторизации с неверным email')
    def test_login_invalid_email(self):
        payload = {
            'email': generators.generate_email(),
            'password': data.UserData.USER_PASSWORD
        }
        with allure.step('Авторизация с неверным email'):
            response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload)  
        assert response.status_code == 401
        assert response.json().get('message') == data.ResponseData.RESPONSE_INVALID_LOGIN['message'] 