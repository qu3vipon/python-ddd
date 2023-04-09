from schema import Schema, Or

from display.domain.entity.room import Room
from shared_kernel.domain.value_object import RoomStatus


def test_get_rooms(client, mocker):
    # given
    room_available = Room(number="A", room_status=RoomStatus.AVAILABLE, image_url="img1")
    room_available.id = 1  # Assume that it is allocated from db

    display_query = mocker.MagicMock()
    display_query.get_rooms.return_value = [room_available]

    client.app.container.display.query.override(display_query)

    # when
    response = client.get("/display/rooms", params={"status": RoomStatus.AVAILABLE})

    # then
    display_query.get_rooms.assert_called_once_with(room_status=RoomStatus.AVAILABLE)

    schema = Schema(
        {
            "detail": "ok",
            "result": [
                {
                    "id": 1,
                    "number": "A",
                    "status": RoomStatus.AVAILABLE,
                    "image_url": "img1",
                    "description": Or(str, None),
                }
            ]
        }
    )

    assert schema.is_valid(response.json())
