from datetime import datetime

from schema import Schema

from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.domain.value_object import RoomStatus, ReservationStatus


def test_create_reservation(client, mocker):
    # given
    ROOM_NUMBER = "ROOM-A"
    GUEST_MOBILE = "+82-10-1111-2222"
    GUEST_NAME = "Guido"

    new_reservation = Reservation(
        room=Room(
            number=ROOM_NUMBER,
            room_status=RoomStatus.AVAILABLE,
        ),
        reservation_number=ReservationNumber.generate(),
        reservation_status=ReservationStatus.IN_PROGRESS,
        date_in=datetime(2023, 4, 1),
        date_out=datetime(2023, 4, 2),
        guest=Guest(
            mobile=GUEST_MOBILE,
            name=GUEST_NAME,
        ),
    )

    reservation_cmd = mocker.MagicMock()
    reservation_cmd.make_reservation.return_value = new_reservation
    with client.app.container.reception.reservation_command.override(reservation_cmd):
        # when
        response = client.post(
            "/reception/reservations",
            json={
                "room_number": ROOM_NUMBER,
                "date_in": "2023-04-01T00:00:00",
                "date_out": "2023-04-02T00:00:00",
                "guest_mobile": GUEST_MOBILE,
                "guest_name": GUEST_NAME,
            }
        )

        # then
        schema = Schema(
            {
                "detail": "ok",
                "result": {
                    "room": {
                        "number": ROOM_NUMBER,
                        "status": RoomStatus.AVAILABLE,
                    },
                    "reservation_number": new_reservation.reservation_number.value,
                    "status": ReservationStatus.IN_PROGRESS,
                    "date_in": "2023-04-01T00:00:00",
                    "date_out": "2023-04-02T00:00:00",
                    "guest": {
                        "mobile": GUEST_MOBILE,
                        "name": GUEST_NAME,
                    }
                }
            }
        )
        assert response.status_code == 201
        assert schema.validate(response.json())


# get reservation

# update guest info

# check in

# check out

# cancel