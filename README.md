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
  """
  Root entity of all the operations.
  """
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
    # ...

  def check_in(self):
    # ...

  def check_out(self):
    # ...

  def change_guest(self, guest: Guest):
    # ...
```

#### Entity: Table Mapping

#### Value Object
```python
from pydantic import constr


mobile_type = constr(regex=r"\+[0-9]{2,3}-[0-9]{2}-[0-9]{4}-[0-9]{4}")

@dataclass(slots=True)
class Guest:
    mobile: mobile_type
    name: Optional[str] = None
```

#### Service

#### Repository

#### DTO(Data Transfer Object)
