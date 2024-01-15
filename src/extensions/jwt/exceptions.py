from extensions.fastapi import APIException


class ApiSignatureExpired(APIException):
    error_message = '此请求已过期'
    error_type = 'api_signature_expired'


class JsonError(APIException):
    error_message = 'secrete key错误'
    error_type = 'json_error'


class AlgorithmError(APIException):
    error_type = 'algorithm_error'
    error_message = '加密算法使用错误'


class JwtTokenError(APIException):
    error_type = 'jwt_token_error'
    error_message = 'jwt token解析错误'
