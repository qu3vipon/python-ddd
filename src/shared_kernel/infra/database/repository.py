from fastapi import Depends
from sqlalchemy.orm import Session

from shared_kernel.domain.entity import EntityType
from shared_kernel.infra.database.connection import get_db


class RDBRepository:
    def __init__(self, session=Depends(get_db)):
        self.session: Session = session

    def add(self, instance: EntityType) -> None:
        self.session.add(instance)

    def commit(self) -> None:
        self.session.commit()


class RDBReadRepository:
    def __init__(self, session=Depends(get_db)):
        self.session: Session = session
