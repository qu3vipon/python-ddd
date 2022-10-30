from dataclasses import field
from typing import Any, TypeVar

EntityType = TypeVar("EntityType", bound="Entity")


class FactoryOnly:
    def __init__(self, direct=True):
        if direct:
            raise ValueError("You can't instantiate it directly.")


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
