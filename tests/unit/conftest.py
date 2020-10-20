from datetime import datetime, timedelta

import pytest
import pytz
from django.utils import timezone


@pytest.fixture
def hour():
    def _dt(hours: float = 0):
        return datetime(2020, 8, 1, 10, 0, 0, tzinfo=pytz.UTC) + timedelta(
            minutes=hours * 60
        )

    return _dt


@pytest.fixture
def hournow():
    def _dt(hours: int = 0):
        return timezone.localtime(timezone.now()) + timedelta(hours=hours)

    return _dt
