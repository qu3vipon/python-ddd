import datetime

from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest


def test_make_reservation(test_session, room_display):
    # given
    room = test_session.query(Room).first()

    # when
    new_reservation = Reservation.make(
        room=room,
        date_in=datetime.datetime(2023, 4, 1),
        date_out=datetime.datetime(2023, 4, 2),
        guest=Guest(
            mobile="+82-10-1111-2222",
            name="Guido",
        )
    )

    test_session.add(new_reservation)
    test_session.commit()

    # then
    assert test_session.query(Reservation).filter(
        Reservation.room == room
    ).first()
