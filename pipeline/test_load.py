# pylint: skip-file
import pytest
import pandas as pd
from unittest.mock import MagicMock
from load import get_foreign_key, get_all_plant_foreign_keys, insert_into_plant_table, insert_into_recording_table


@pytest.fixture
def mock_db_cursor():
    """Fixture to mock the database cursor."""
    mock_cursor = MagicMock()
    return mock_cursor


@pytest.fixture
def mock_connection():
    """Fixture to mock the database connection."""
    mock_conn = MagicMock()
    return mock_conn


@pytest.fixture
def mock_get_foreign_key(mocker):
    """Fixture to mock the get_foreign_key function."""
    return mocker.patch('load.get_foreign_key')


def test_get_foreign_key_success(mock_db_cursor):
    mock_db_cursor.fetchone.return_value = (1,)

    result = get_foreign_key(mock_db_cursor, 'botanist',
                             'botanist_email', 'random.dude@email.com')
    assert result == 1
    mock_db_cursor.execute.assert_called_once_with(
        "SELECT * FROM None.botanist WHERE botanist_email = %s", (
            'random.dude@email.com',)
    )


def test_get_foreign_key_failure(mock_db_cursor):
    mock_db_cursor.fetchone.return_value = None

    email = 'nonexistent.email@email.com'

    with pytest.raises(ValueError, match='Invalid Data!'):
        get_foreign_key(mock_db_cursor, 'botanist', 'botanist_email', email)

    mock_db_cursor.execute.assert_called_once_with(
        f"SELECT * FROM None.botanist WHERE botanist_email = %s", (email,))


def test_get_all_plant_foreign_keys_success(mock_db_cursor, mock_get_foreign_key):
    data = {
        'botanist_email': ['botanist1@email.com', 'botanist2@email.com'],
        'plant_name': ['Plant A', 'Plant B'],
        'country_code': ['US', 'CA']
    }
    df = pd.DataFrame(data)

    mock_get_foreign_key.side_effect = [
        1,
        10,
        100,
        2,
        20,
        200
    ]

    result = get_all_plant_foreign_keys(mock_db_cursor, df)

    expected_result = [
        (1, 10, 100),
        (2, 20, 200)
    ]

    assert result == expected_result

    assert mock_get_foreign_key.call_count == 6
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'botanist', 'botanist_email', 'botanist1@email.com')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'species', 'plant_name', 'Plant A')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'country', 'country_code', 'US')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'botanist', 'botanist_email', 'botanist2@email.com')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'species', 'plant_name', 'Plant B')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'country', 'country_code', 'CA')


def test_insert_into_plant_table(mock_db_cursor, mock_connection, mock_get_foreign_key):
    data = {
        'botanist_email': ['botanist1@email.com', 'botanist2@email.com'],
        'plant_name': ['Plant A', 'Plant B'],
        'country_code': ['US', 'UK']
    }
    df = pd.DataFrame(data)

    mock_get_foreign_key.return_value = 1

    mock_db_cursor.execute.return_value = None

    mock_db_cursor.fetchone.side_effect = [(1,), (2,)]

    plant_ids = insert_into_plant_table(mock_connection, mock_db_cursor, df)

    assert plant_ids == [1, 2], "Plant IDs should be [1, 2]"

    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'botanist', 'botanist_email', 'botanist1@email.com')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'species', 'plant_name', 'Plant A')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'country', 'country_code', 'US')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'botanist', 'botanist_email', 'botanist2@email.com')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'species', 'plant_name', 'Plant B')
    mock_get_foreign_key.assert_any_call(
        mock_db_cursor, 'country', 'country_code', 'UK')

    mock_db_cursor.execute.assert_any_call("SELECT SCOPE_IDENTITY()")
    assert mock_db_cursor.execute.call_count == 4


def test_insert_into_recording_table(mock_db_cursor, mock_connection):
    data = {
        'recording_taken': ['2024-11-01', '2024-11-02'],
        'last_watered': ['2024-11-01', '2024-11-02'],
        'soil_moisture': [30, 40],
        'temperature': [22.5, 25.0],
    }
    df = pd.DataFrame(data)

    plant_ids = [1, 2]

    mock_db_cursor.execute.return_value = None
    mock_db_cursor.commit.return_value = None

    insert_into_recording_table(mock_connection, mock_db_cursor, df, plant_ids)

    for index, row in df.iterrows():
        expected_query = """
                        INSERT INTO recording (plant_id, recording_taken, last_watered, soil_moisture, temperature) VALUES
                        (%s, %s, %s, %s, %s)"""

        expected_args = (plant_ids[index], row['recording_taken'],
                         row['last_watered'], row['soil_moisture'], row['temperature'])

        mock_db_cursor.execute.assert_any_call(expected_query, expected_args)

        mock_db_cursor.commit()

    assert mock_db_cursor.commit.call_count == len(
        df), f"Expected {len(df)} commits"
