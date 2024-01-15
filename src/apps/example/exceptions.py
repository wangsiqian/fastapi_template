from extensions.fastapi import APIException


class PersonNotFound(APIException):
    error_type = 'person_not_found'
    error_message = 'Person not found'


class PersonAlreadyExist(APIException):
    error_type = 'person_already_exist'
    error_message = 'Person already exist'
