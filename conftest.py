import requests
import generators
import data
import pytest
from curls import Curls

def _bearer(token: str) -> dict:
    """Единая сборка заголовка авторизации."""
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture()
def generate_data_and_delete_user():
    """
    Создаём тестового пользователя и удаляем его после теста.
    Изменение: все запросы через json=, а Auth — через Bearer.
    """
    payload = {
        'email': generators.generate_email(),
        'password': generators.generate_password(),
        'name': generators.generate_name()
    }
    # Пользователь создаётся уже в самом тесте (там POST /register),
    # здесь только возвращаем готовое тело для регистрации.
    yield payload

    # После теста — логинимся и удаляем созданного пользователя (если он есть).
    payload_login = {'email': payload['email'], 'password': payload['password']}
    resp_login = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload_login)  
    if resp_login.status_code == 200 and 'accessToken' in resp_login.json():
        token = resp_login.json()['accessToken']
        requests.delete(f'{Curls.MAIN_URL}{Curls.URL_DELETE_USER}', headers=_bearer(token))

@pytest.fixture(scope='session')
def login_user():
    """
    Логин фиксированным пользователем из data.UserData.
    Возвращает тело ответа (включая accessToken).
    """
    payload = {'email': data.UserData.USER_EMAIL, 'password': data.UserData.USER_PASSWORD}
    response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload)  
    response.raise_for_status()
    return response.json()

@pytest.fixture()
def login_and_return_data():
    """
    Логин пользователем для сценариев изменения профиля.
    После теста откатываем имя обратно.
    """
    payload = {
        'email': data.UserDataForChange.USER_EMAIL,
        'password': data.UserDataForChange.USER_PASSWORD
    }
    response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload)  
    response.raise_for_status()
    auth_body = response.json()
    yield auth_body

    # Откат имени
    return_name = {'email': data.UserDataForChange.USER_EMAIL, 'name': data.UserDataForChange.USER_NAME}
    requests.patch(
        f'{Curls.MAIN_URL}{Curls.URL_CHANGE_USER_DATA}',
        json=return_name, 
        headers=_bearer(auth_body['accessToken'])
    )

@pytest.fixture(scope='session')
def get_ingredients():
    """
    Возвращает список валидных id ингредиентов.
    Изменение: используем Curls.MAIN_URL, а не жёсткий домен; JSON парсинг.
    """
    resp = requests.get(f'{Curls.MAIN_URL}/api/ingredients')  
    resp.raise_for_status()
    body = resp.json()
    return [item['_id'] for item in body.get('data', [])]

