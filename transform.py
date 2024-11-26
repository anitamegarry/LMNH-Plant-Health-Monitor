"""Script that will ensure the data follows the database schema."""
import pandas as pd
from extract import load_into_dataframe


def convert_columns_to_datetime(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Converts recording_taken and last_watered
       To type datetime."""
    dataframe['recording_taken'] = pd.to_datetime(
        dataframe['recording_taken'], errors='coerce').dt.tz_localize('UTC', ambiguous='NaT')
    dataframe['last_watered'] = pd.to_datetime(
        dataframe['last_watered'], errors='coerce').dt.tz_convert('UTC')

    return dataframe


if __name__ == "__main__":
    plant_dataframe = load_into_dataframe()
    convert_columns_to_datetime(plant_dataframe)
