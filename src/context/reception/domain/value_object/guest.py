from __future__ import annotations

from typing import Optional

from context.shared_kernel.domain import FactoryOnly


class Guest(FactoryOnly):
    def __init__(self, mobile: str, name: Optional[str], **kwargs):
        super().__init__(**kwargs)
        self.mobile = mobile
        self.name = name

    @classmethod
    def generate(cls, mobile: str, name: Optional[str] = None) -> Guest:
        return cls(mobile=mobile, name=name, direct=False)
