from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pydantic import constr

from bounded_context.shared_kernel.value_object import ValueObject

mobile_type = constr(regex=r"\+[0-9]{2,3}-[0-9]{2}-[0-9]{4}-[0-9]{4}")


@dataclass(slots=True)
class Guest(ValueObject):
    mobile: mobile_type
    name: Optional[str] = None

    def __composite_values__(self):
        return self.mobile, self.name
