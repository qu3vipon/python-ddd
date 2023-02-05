from shared_kernel.domain.entity import EntityType


class RDBRepository:
    @staticmethod
    def add(session, instance: EntityType):
        return session.add(instance)

    @staticmethod
    def commit(session):
        return session.commit()


class RDBReadRepository:
    pass
