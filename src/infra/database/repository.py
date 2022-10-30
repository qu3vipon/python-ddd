from fastapi import Depends
from sqlalchemy.orm import Session

from context.shared_kernel.domain import EntityType
from infra.database.connection import get_db


class RDBRepository:
    def __init__(self, session=Depends(get_db)):
        self.session: Session = session

    def add(self, instance: EntityType) -> None:
        return self.session.add(instance)

    def commit(self) -> None:
        return self.session.commit()

    def refresh(self, instance: EntityType) -> None:
        return self.session.refresh(instance)
