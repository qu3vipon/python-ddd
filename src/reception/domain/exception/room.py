from shared_kernel.application.exception import BaseMsgException


class RoomNotFoundException(BaseMsgException):
    message = "Room is not found."


class RoomStatusException(BaseMsgException):
    message = "Invalid request for current room status."
