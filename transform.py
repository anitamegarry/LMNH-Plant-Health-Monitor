"""Script that will ensure the data follows the database schema."""
import re
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


def clean_name(name: str) -> str:
    """Removes any non alphabet characters
        And makes the name lower case."""
    if isinstance(name, str):
        cleaned_name = re.sub(r'[^a-zA-Z\s]', '', name)
        return ' '.join(cleaned_name.split()).lower()
    return name


def clean_plant_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Cleans the name of all values within the plant_name column."""
    dataframe["plant_name"] = dataframe['plant_name'].apply(clean_name)
    return dataframe


if __name__ == "__main__":
    plant_dataframe = load_into_dataframe()
    convert_columns_to_datetime(plant_dataframe)
    plant_dataframe = clean_plant_names(plant_dataframe)
