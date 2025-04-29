
class MyException(Exception):
    """Raised when ...MyException"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Default Message'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class UserAlreadyExists(Exception):
    """Raised when user already exists in table"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'User already exists in table.'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class RegistrationCancelled(Exception):
    """Raised when registration cancelled"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Registration cancelled'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class IncorrectInputData(Exception):
    """Raised when incorrect data was passed"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Incorrect Input Data'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class EventNameIsTooLong(Exception):
    """Raised when event na,e is too long"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Event Name Is Too Long'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class UserTooYoung(Exception):
    """Raised when user is too young"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'User is too young'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class IncorrectApplicationData(Exception):
    """Raised when incorrect data was passed"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Incorrect application Data'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class UserNotRegistered(Exception):
    """Raised when User is not registered"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'User is not registered'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class ApplicationAlreadyExists(Exception):
    """Raised when Application already exists"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Application already exists'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class InputCancelled(Exception):
    """Raised when Input Cancelled"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Input Cancelled'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class WrongDocumentType(Exception):
    """Raised when passing the wrong document type"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Wrong Document Type'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class NoFileAttached(Exception):
    """Raised when no file attached to the message"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'No File Attached'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)
