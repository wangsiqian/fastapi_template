from extensions.fastapi import APIException


class UserNotFound(APIException):
    error_type = 'user_not_found'
    error_message = '请先创建您的账号'


class AccountOrPasswordWrong(APIException):
    error_type = 'account_or_password_wrong'
    error_message = '账号或者密码错误'


class UserAlreadyExist(APIException):
    error_type = 'user_already_exist'
    error_message = '用户已经存在'
