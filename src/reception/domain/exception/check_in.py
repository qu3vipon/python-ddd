from shared_kernel.application.exception import BaseMsgException


class CheckInDateException(BaseMsgException):
    message = "Invalid date for check-in."


class CheckInAuthenticationException(BaseMsgException):
    message = "Invalid guest authentication for check-in."
