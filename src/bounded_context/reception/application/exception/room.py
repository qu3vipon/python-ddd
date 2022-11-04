from bounded_context.shared_kernel.exception import BaseError


class RoomNotFoundError(BaseError):
    message = "Room is not found."


class RoomStatusError(BaseError):
    message = "Invalid request for current room status."
