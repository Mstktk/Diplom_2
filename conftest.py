import requests
import generators
import data
import pytest
from curls import Curls

def _bearer(token: str) -> dict:
    """
    Нормализация: если сервер уже вернул 'Bearer <jwt>' как токен,
    не дублируем префикс в заголовке.
    """
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture()
def generate_data_and_delete_user():
    payload = {
        'email': generators.generate_email(),
        'password': generators.generate_password(),
        'name': generators.generate_name()
    }
    yield payload

    # Чистим — если пользователь создан
    payload_login = {'email': payload['email'], 'password': payload['password']}
    resp_login = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload_login)
    if resp_login.status_code == 200 and 'accessToken' in resp_login.json():
        token = resp_login.json()['accessToken']
        requests.delete(f'{Curls.MAIN_URL}{Curls.URL_DELETE_USER}', headers=_bearer(token))

@pytest.fixture(scope='session')
def login_user():
    payload = {'email': data.UserData.USER_EMAIL, 'password': data.UserData.USER_PASSWORD}
    response = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=payload)
    response.raise_for_status()
    return response.json()

@pytest.fixture()
def login_and_return_data():
    """
    Логинимся пользователем для тестов изменения профиля.
    Если пользователя ещё нет — создаём и логинимся повторно.
    """
    creds = {
        'email': data.UserDataForChange.USER_EMAIL,
        'password': data.UserDataForChange.USER_PASSWORD
    }
    resp = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=creds)
    if resp.status_code == 401:
        # создаём пользователя
        reg_payload = {
            'email': data.UserDataForChange.USER_EMAIL,
            'password': data.UserDataForChange.USER_PASSWORD,
            'name': data.UserDataForChange.USER_NAME
        }
        reg = requests.post(f'{Curls.MAIN_URL}{Curls.URL_REGISTRATION}', json=reg_payload)
        reg.raise_for_status()
        # логинимся снова
        resp = requests.post(f'{Curls.MAIN_URL}{Curls.URL_LOGIN}', json=creds)

    resp.raise_for_status()
    auth_body = resp.json()

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
    resp = requests.get(f'{Curls.MAIN_URL}/api/ingredients')
    resp.raise_for_status()
    body = resp.json()
    return [item['_id'] for item in body.get('data', [])]

