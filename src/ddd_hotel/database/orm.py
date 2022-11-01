from sqlalchemy import MetaData, Table, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry()


room_table = Table(
    "hotel_room",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number", String(20), nullable=False),
    Column("status", String(10), nullable=False),
    Column("image_url", String(200), nullable=False),
    Column("description", Text, nullable=True),
)

reservation_table = Table(
    "room_reservation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("room_id", Integer, ForeignKey("hotel_room.id"), nullable=False),
    Column("number", String(20), nullable=False),
    Column("date_in", DateTime(timezone=True)),
    Column("date_out", DateTime(timezone=True)),
    Column("guest_mobile", String(20), nullable=False),
    Column("guest_name", String(50), nullable=False),
)


def init_orm_mappers():
    """
    initialize orm mappings
    """
    from bounded_context.reception.domain.entity.room import Room as ReceptionRoomEntity
    from bounded_context.reception.domain.entity.reservation import Reservation as ReceptionReservationEntity

    mapper_registry.map_imperatively(ReceptionRoomEntity, room_table)
    mapper_registry.map_imperatively(ReceptionReservationEntity, reservation_table)
