class AuthError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Неправильные данные. Попробуйте снова'


class NeedRefreshToken(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Need refresh token'


class ServerError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Ошибка сервера. Попробуйте позже'


class EmptyField(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Обязательное поле не заполнено'

