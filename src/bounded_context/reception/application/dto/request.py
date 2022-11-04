from datetime import datetime

from pydantic import BaseModel

from bounded_context.reception.domain.value_object.guest import mobile_type


class CreateReservationRequest(BaseModel):
    room_number: str
    date_in: datetime
    date_out: datetime
    guest_mobile: mobile_type
    guest_name: str | None = None


class UpdateGuestRequest(BaseModel):
    guest_mobile: mobile_type
    guest_name: str | None = None


class CheckInRequest(BaseModel):
    mobile: mobile_type
