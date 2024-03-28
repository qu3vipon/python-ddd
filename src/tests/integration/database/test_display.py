from display.domain.entity.room import Room
from shared_kernel.domain.value_object import RoomStatus


def test_save_room(test_session):
    # given
    assert not test_session.query(Room).first()

    new_room = Room(number="New", room_status=RoomStatus.AVAILABLE, image_url="image_url")

    # when
    test_session.add(new_room)
    test_session.commit()

    # then
    assert test_session.query(Room).filter(
        Room.number == "New",
        Room.room_status == RoomStatus.AVAILABLE,
        Room.image_url == "image_url",
    ).first()
