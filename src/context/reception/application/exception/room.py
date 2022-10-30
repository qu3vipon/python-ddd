from context.shared_kernel.exception import BaseError


class RoomStatusError(BaseError):
    message = "Invalid request for current room status."
