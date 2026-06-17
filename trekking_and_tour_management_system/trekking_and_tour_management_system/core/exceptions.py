# core/exceptions.py

class BusinessLogicException(Exception):
    pass


class ValidationException(Exception):
    pass


class NotFoundException(Exception):
    pass


class PermissionDeniedException(Exception):
    pass