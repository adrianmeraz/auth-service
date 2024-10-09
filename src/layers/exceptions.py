from py_aws_core.exceptions import CoreException


class ASCoreException(CoreException):
    pass


class AuthServiceException(ASCoreException):
    ERROR_MESSAGE = 'Error occurred attempting to access authentication service'
