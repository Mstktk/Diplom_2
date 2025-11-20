def _bearer(token: str) -> dict:
    """
    Нормализация: если сервер уже вернул 'Bearer <jwt>' как токен,
    не дублируем префикс в заголовке.
    """
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]
    return {'Authorization': f'Bearer {token}'}

