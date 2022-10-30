from context.shared_kernel.exception import BaseError


class CheckInDateError(BaseError):
    message = "Invalid date for check-in."


class CheckInAuthenticationError(BaseError):
    message = "Invalid guest authentication for check-in."
