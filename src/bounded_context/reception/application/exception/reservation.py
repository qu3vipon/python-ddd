from bounded_context.shared_kernel.exception import BaseError


class ReservationStatusError(BaseError):
    message = "Invalid request for current reservation status."
