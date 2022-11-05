from shared_kernel.application.exception import BaseError


class RoomNotFoundError(BaseError):
    message = "Room is not found."


class RoomStatusError(BaseError):
    message = "Invalid request for current room status."
