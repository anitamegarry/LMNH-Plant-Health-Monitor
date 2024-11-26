# pylint: skip-file
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd
from extract import get_plant_data, extract_plant_data, load_into_dataframe, TOTAL_NUMBER_OF_PLANTS


@pytest.fixture
def initial_dataframe():
    return pd.DataFrame({
        "botanist_first_name": pd.Series(dtype=str),
        "botanist_last_name": pd.Series(dtype=str),
        "botanist_email": pd.Series(dtype=str),
        "botanist_phone_number": pd.Series(dtype=str),
        "plant_name": pd.Series(dtype=str),
        "plant_scientific_name": pd.Series(dtype=str),
        "recording_taken": pd.Series(dtype=str),
        "last_watered": pd.Series(dtype=str),
        "soil_moisture": pd.Series(dtype=float),
        "temperature": pd.Series(dtype=float),
        "country_code": pd.Series(dtype=str),
    })


def mock_get_success(url):
    """Mock a successful API response"""
    return mock.Mock(status_code=200, json=lambda: {"name": "Epipremnum Aureum"})


def test_get_plant_data_success():
    with mock.patch("requests.get", side_effect=mock_get_success):
        response = get_plant_data(1)
        assert response == {
            "name": "Epipremnum Aureum"}, "Expected successful API response"


def test_extract_plant_data_valid():
    valid_response = {
        "botanist": {
            "name": "Carl Linnaeus",
            "email": "carl.linnaeus@lnhm.co.uk",
            "phone": "(146)994-1635x35992"
        },
        "name": "Epipremnum Aureum",
        "scientific_name": ["Epipremnum aureum"],
        "recording_taken": "2024-11-25 14:19:28",
        "last_watered": "Mon, 25 Nov 2024 14:03:04 GMT",
        "soil_moisture": 99.0464993678606,
        "temperature": 13.15915073027191,
        "origin_location": ["-19.32556", "-41.25528", "Resplendor", "BR"]
    }

    result = extract_plant_data(valid_response)
    expected = {
        "botanist_first_name": "Carl",
        "botanist_last_name": "Linnaeus",
        "botanist_email": "carl.linnaeus@lnhm.co.uk",
        "botanist_phone_number": "(146)994-1635x35992",
        "plant_name": "Epipremnum Aureum",
        "plant_scientific_name": "Epipremnum aureum",
        "recording_taken": "2024-11-25 14:19:28",
        "last_watered": "Mon, 25 Nov 2024 14:03:04 GMT",
        "soil_moisture": 99.0464993678606,
        "temperature": 13.15915073027191,
        "country_code": "BR"
    }
    assert result == expected


def test_extract_plant_data_missing_botanist():
    response_missing_botanist = {
        "name": "Epipremnum Aureum",
        "scientific_name": ["Epipremnum aureum"],
        "recording_taken": "2024-11-25 14:19:28",
        "last_watered": "Mon, 25 Nov 2024 14:03:04 GMT",
        "soil_moisture": 99.0464993678606,
        "temperature": 13.15915073027191,
        "origin_location": ["-19.32556", "-41.25528", "Resplendor", "BR"]
    }
    result = extract_plant_data(response_missing_botanist)
    expected = {
        "botanist_first_name": None,
        "botanist_last_name": None,
        "botanist_email": None,
        "botanist_phone_number": None,
        "plant_name": "Epipremnum Aureum",
        "plant_scientific_name": "Epipremnum aureum",
        "recording_taken": "2024-11-25 14:19:28",
        "last_watered": "Mon, 25 Nov 2024 14:03:04 GMT",
        "soil_moisture": 99.0464993678606,
        "temperature": 13.15915073027191,
        "country_code": "BR"
    }
    assert result == expected


@patch('multiprocessing.Pool')
def test_load_into_dataframe(mock_pool_class, initial_dataframe):
    mock_plant_data = {
        "botanist_first_name": "Carl",
        "botanist_last_name": "Linnaeus",
        "botanist_email": "carl.linnaeus@lnhm.co.uk",
        "botanist_phone_number": "(146)994-1635x35992",
        "plant_name": "Epipremnum Aureum",
        "plant_scientific_name": "Epipremnum aureum",
        "recording_taken": "2024-11-25 14:19:28",
        "last_watered": "Mon, 25 Nov 2024 14:03:04 GMT",
        "soil_moisture": 99.0464993678606,
        "temperature": 13.15915073027191,
        "country_code": "BR",
    }

    mock_pool_instance = MagicMock()
    mock_pool_class.return_value = mock_pool_instance

    mock_pool_instance.map.return_value = [
        mock_plant_data] * (TOTAL_NUMBER_OF_PLANTS + 1)

    result_dataframe = load_into_dataframe(initial_dataframe)

    assert "botanist_first_name" in result_dataframe.columns
    assert "plant_name" in result_dataframe.columns

    assert result_dataframe["botanist_first_name"].iloc[0] == "Carl"
    assert result_dataframe["botanist_last_name"].iloc[0] == "Linnaeus"
    assert result_dataframe["plant_name"].iloc[0] == "Epipremnum Aureum"
    assert result_dataframe["country_code"].iloc[0] == "BR"
