from datetime import date

import pytest
from fastapi import HTTPException

from app.routes.reports import weekly_sales


def test_rejects_inverted_dates():
    with pytest.raises(HTTPException) as exc:
        weekly_sales(date(2026, 6, 10), date(2026, 6, 1))

    assert exc.value.status_code == 422


def test_rejects_more_than_seven_days():
    with pytest.raises(HTTPException) as exc:
        weekly_sales(date(2026, 6, 1), date(2026, 6, 8))

    assert exc.value.status_code == 422
