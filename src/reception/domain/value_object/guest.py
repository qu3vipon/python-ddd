from __future__ import annotations

from dataclasses import dataclass

from pydantic import constr

from shared_kernel.domain.value_object import ValueObject

mobile_type = constr(regex=r"\+[0-9]{2,3}-[0-9]{2}-[0-9]{4}-[0-9]{4}")


@dataclass(slots=True)
class Guest(ValueObject):
    mobile: mobile_type
    name: str | None = None

    def __composite_values__(self):
        return self.mobile, self.name
