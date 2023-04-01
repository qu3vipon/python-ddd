from datetime import datetime, date

import pytest
from fastapi.testclient import TestClient
from schema import And, Use

from shared_kernel.infra.fastapi.main import app


@pytest.fixture
def client():
    return TestClient(app)


valid_datetime = And(Use(lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")), datetime)
valid_date = And(Use(lambda s: datetime.strptime(s, "%Y-%m-%d").date()), date)
