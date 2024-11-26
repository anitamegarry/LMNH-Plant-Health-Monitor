# pylint: skip-file
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from transform import convert_columns_to_datetime


def test_convert_columns_to_datetime():
    input_data = pd.DataFrame({
        "recording_taken": ["2024-11-25 15:30:00", "invalid_date", None],
        "last_watered": [
            pd.Timestamp("2024-11-25 12:00:00", tz="UTC"),
            pd.Timestamp("2024-11-26 08:45:00", tz="UTC"),
            None
        ]
    })

    expected = pd.DataFrame({
        "recording_taken": [
            pd.to_datetime("2024-11-25 15:30:00").tz_localize("UTC"),
            pd.NaT,
            pd.NaT
        ],
        "last_watered": [
            pd.to_datetime("2024-11-25 12:00:00", utc=True),
            pd.to_datetime("2024-11-26 08:45:00", utc=True),
            pd.NaT
        ]
    })

    result_data = convert_columns_to_datetime(input_data)

    assert_frame_equal(result_data, expected, check_dtype=True)
