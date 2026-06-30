from datetime import date

import pandas as pd

from src.ui.pages import _filter_dataframe_by_date


def test_filter_dataframe_by_date_uses_available_timestamp():
    frame = pd.DataFrame(
        {
            "created_at": ["2026-06-01T10:00:00", "2026-06-15T12:00:00", "2026-07-01T08:00:00"],
            "value": [1, 2, 3],
        }
    )

    result = _filter_dataframe_by_date(frame, (date(2026, 6, 10), date(2026, 6, 30)))

    assert result["value"].tolist() == [2]


def test_filter_dataframe_by_date_excludes_invalid_dates():
    frame = pd.DataFrame({"created_at": ["invalid", "2026-06-30"], "value": [1, 2]})

    result = _filter_dataframe_by_date(frame, (date(2026, 6, 1), date(2026, 6, 30)))

    assert result["value"].tolist() == [2]


def test_filter_dataframe_by_date_preserves_frame_without_date_column():
    frame = pd.DataFrame({"value": [1, 2]})

    result = _filter_dataframe_by_date(frame, (date(2026, 6, 1), date(2026, 6, 30)))

    assert result.equals(frame)
    assert result is not frame
