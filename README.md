# [WIP] Python Domain-Driven-Design(DDD) Example

## Intro
I have adopted the DDD pattern for my recent FastAPI project.
DDD makes it easier to implement complex domain problems.
Improved readability and easier code modification have greatly increased productivity.
As a result, stable service and project management have become possible.
I'm very satisfied with it, so I want to share this experience and knowledge.

### Why DDD?
Using DDD makes it easy to maintain collaboration with domain experts, not only engineers.
- It is possible to prevent the mental model and the actually implemented software from being dualized.
- Business logic is easy to manage.
- Infrastructure change is flexible.


### Objective
- Let's create a simple hotel reservation system and see how each component of DDD is implemented.
- Don't go too deep into topics like CQRS or event sourcing.
- Considering the running curve, this project consists only of essential DDD components. 
  - excluded: UoW, Use cases, etc.

## Implementation
### ERD
> NOTES: The diagram below represents only the database tables.

![erd](./docs/image/erd.png)

### Bounded Context

![bounded-context](./docs/image/bounded-context.png)

- Display (Handling tasks related to the hotel room display)
  - List Rooms 
  - Add a Room
- Reception (Handling tasks related to the hotel room reservation)
  - Make a reservation
  - Change the reservation details
  - Cancel a reservation
  - Check-in & Check-out

Check-in & check-out domains can also be isolated, but let's say that reception handles it together for now.

### Project Structure
```tree
src
├── bounded_context
│   ├── display
│   │   ├── application
│   │   │   ├── dto
│   │   │   ├── exception
│   │   │   └── service
│   │   ├── domain
│   │   │   ├── entity
│   │   │   └── value_object
│   │   ├── infra
│   │   │   ├── repository
│   │   │   └── external_apis
│   │   ├── presentation
│   │   │   ├── grpc
│   │   │   └── rest
│   │   └── test
│   ├── reception
│   │   ├── application
│   │   ├── domain
│   │   ├── infra
│   │   ├── presentation
│   │   └── test
│   └── shared_kernel
└── ddd_hotel
    ├── database
    │   ├── connection
    │   ├── orm
    │   └── repository
    ├── fastapi
    │   ├── config
    │   └── main.py 
    └── log
```

### DDD Components
#### Entity: Definition
```python
from dataclasses import dataclass, field


class Entity:
    id: int = field(init=False)
  
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False
  
    def __hash__(self):
        return hash(self.id)


class AggregateRoot(Entity):
    pass


@dataclass(eq=False, slots=True)
class Reservation(AggregateRoot):
    room: Room
    reservation_number: ReservationNumber
    status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: Guest
```

1. Entity mix-in <br>
The entity is an object that have a distinct identity.
I will implement `__eq__()` and `__hash__()`, to use it as a mix-in for dataclass.

2. Aggregate Root <br>
A DDD aggregate is a cluster of domain objects that can be treated as a single unit.
An aggregate root is an entry point of an aggregate.
Any references from outside the aggregate should only go to the aggregate root. 
The root can thus ensure the integrity of the aggregate as a whole. 
I will define an empty class called `AggregateRoot` and explicitly mark it.

3. Entity Class <br>
To use `__eq__()` from `Entity` mix-in, add `eq=False`.
From Python 3.10, `slots=True` makes dataclass more memory-efficient.

#### Entity: Life Cycle

```python
@dataclass(eq=False, slots=True)
class Reservation(AggregateRoot):
    # ...

    @classmethod
    def make(cls, room: Room, date_in: datetime, date_out: datetime, guest: Guest) -> Reservation:
        room.reserve()
        return cls(
            room=room,
            date_in=date_in,
            date_out=date_out,
            guest=guest,
            reservation_number=ReservationNumber.generate(),
            status=ReservationStatus.IN_PROGRESS,
        )

    def cancel(self):
        if not self.status.in_progress():
            raise ReservationStatusError
  
        self.status = ReservationStatus.CANCELLED
  
    def check_in(self):
        # ...
  
    def check_out(self):
        # ...
  
    def change_guest(self, guest: Guest):
        # ...
```

By implementing the method according to the entity changes, you can visually check the life cycle of it.


1. Creation <br>
Declare a class method and use it when creating an entity.

2. Changes <br>
Declare an instance method and use it when changing an entity.

#### Entity: Table Mapping
- [ddd_hotel/database/orm.py](src/ddd_hotel/database/orm.py)
```python
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
    Column("date_in", DateTime(timezone=True), nullable=False),
    Column("date_out", DateTime(timezone=True), nullable=False),
    Column("guest_mobile", String(20), nullable=False),
    Column("guest_name", String(50), nullable=True),
)


def init_orm_mappers():
    from bounded_context.reception.domain.entity.room import Room as ReceptionRoomEntity
    from bounded_context.reception.domain.entity.reservation import Reservation as ReceptionReservationEntity
    
    from bounded_context.display.domain.entity.room import Room as DisplayRoomEntity
    from bounded_context.display.domain.entity.reservation import Reservation as DisplayReservationEntity

    
    mapper_registry.map_imperatively(ReceptionRoomEntity, room_table)
    mapper_registry.map_imperatively(ReceptionReservationEntity, reservation_table)

    mapper_registry.map_imperatively(DisplayRoomEntity, room_table)
    mapper_registry.map_imperatively(DisplayReservationEntity, reservation_table)
```
Because entities do not need to know the implementation of the database table, let's use sqlalchemy's [imperative mapping](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#imperative-mapping) to separate entity definitions and table definitions.
Entities only need to use logically required data among the columns defined in the table.

```python
# call this after app running
init_orm_mappers()
```    


#### Value Object
```python
from pydantic import constr


mobile_type = constr(regex=r"\+[0-9]{2,3}-[0-9]{2}-[0-9]{4}-[0-9]{4}")

@dataclass(slots=True)
class Guest:
    mobile: mobile_type
    name: Optional[str] = None
```

The value object is an object that matter only as the combination of their attributes.
Guest A's name and mobile should be treated as a single unit, so make it a value object.

#### Dependency Injection (Service & Repository)

#### DTO(Data Transfer Object)
