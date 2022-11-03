from dataclasses import field
from enum import EnumMeta
from typing import Any, TypeVar, Optional

EntityType = TypeVar("EntityType", bound="Entity")
ValueObjectType = TypeVar("ValueObjectType", bound="ValueObject")


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
    An entry point of aggregate.
    """
    pass


class ValueObject:
    def __composite_values__(self):
        return self.value,

    @classmethod
    def from_value(cls, v: Any) -> Optional[ValueObjectType]:
        if isinstance(cls, EnumMeta):
            for item in cls:
                if item.value == v:
                    return item
            return None
        else:
            return cls(value=v)
