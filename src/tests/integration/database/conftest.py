import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from shared_kernel.infra.database.orm import metadata


@pytest.fixture(scope="session")
def test_db():
    test_db_url = "mysql+pymysql://admin:ddd-hotel@127.0.0.1:3306/ddd-hotel"
    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    metadata.create_all(engine)
    try:
        yield engine
    finally:
        metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    connection = test_db.connect()

    trans = connection.begin()
    session = sessionmaker()(bind=connection)

    session.begin_nested()  # SAVEPOINT

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
    trans.rollback()  # roll back to the SAVEPOINT
    connection.close()


@pytest.fixture
def room_display(test_session):
    from display.domain.entity.room import Room
    from shared_kernel.domain.value_object import RoomStatus

    room = Room(number="New", room_status=RoomStatus.AVAILABLE, image_url="image_url")
    test_session.add(room)
    test_session.commit()
    return room
