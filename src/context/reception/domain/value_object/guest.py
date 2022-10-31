from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pydantic import constr


mobile_type = constr(regex=r"\+[0-9]{2,3}-[0-9]{2}-[0-9]{4}-[0-9]{4}")


@dataclass(slots=True)
class Guest:
    mobile: mobile_type
    name: Optional[str] = None
