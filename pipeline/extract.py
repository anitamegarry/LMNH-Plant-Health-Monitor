"""Script that connects to 'data-eng-plants-api'
   Extracts the data
   Puts it into a Pandas DataFrame"""
from multiprocessing import Pool, cpu_count
from typing import Optional
import requests
import pandas as pd

URL = "https://data-eng-plants-api.herokuapp.com/plants/"
TOTAL_NUMBER_OF_PLANTS = 50


def get_plant_data(plant_id: int) -> dict:
    """GET request to collect plant data from API."""
    response = requests.get(URL + str(plant_id), timeout=30)
    if response.status_code == 200:
        return response.json()
    return {"error": response.status_code,
            "message": f"Failed to retrieve data for plant ID {plant_id}."}


def extract_plant_data(response: dict) -> dict:
    """Extracts plant data from the API response and handles missing fields."""
    botanist_name = response.get("botanist", {}).get("name", "").split()
    plant_name = response.get("name") or response.get(
        "scientific_name") or None
    return {
        "botanist_first_name": botanist_name[0] if len(botanist_name) > 0 else None,
        "botanist_last_name": botanist_name[1] if len(botanist_name) > 1 else None,
        "botanist_email": response.get("botanist", {}).get("email"),
        "botanist_phone_number": response.get("botanist", {}).get("phone"),
        "plant_name": plant_name,
        "recording_taken": response.get("recording_taken"),
        "last_watered": response.get("last_watered"),
        "soil_moisture": response.get("soil_moisture"),
        "temperature": response.get("temperature"),
        "country_code": response.get("origin_location", [None, None, None, None])[3],
        "plant_id": response.get("plant_id")
    }


def fetch_and_extract_plant_data(plant_id: int) -> Optional[dict]:
    """Fetches plant data and extracts relevant fields."""
    response = get_plant_data(plant_id)
    if "error" in response:
        return None
    return extract_plant_data(response)


def initialise_dataframe() -> pd.DataFrame:
    """Creates the initial, empty DataFrame with columns."""
    return pd.DataFrame({
        "botanist_first_name": pd.Series(dtype=str),
        "botanist_last_name": pd.Series(dtype=str),
        "botanist_email": pd.Series(dtype=str),
        "botanist_phone_number": pd.Series(dtype=str),
        "plant_name": pd.Series(dtype=str),
        "recording_taken": pd.Series(dtype=str),
        "last_watered": pd.Series(dtype=str),
        "soil_moisture": pd.Series(dtype=float),
        "temperature": pd.Series(dtype=float),
        "country_code": pd.Series(dtype=str),
        "plant_id": pd.Series(dtype=int)
    })


# def load_into_dataframe() -> pd.DataFrame:
#     """Fetches API data for all plants using multiprocessing and appends it to a DataFrame."""
#     plant_dataframe = initialise_dataframe()
#     with Pool(processes=cpu_count()) as pool:
#         results = pool.map(fetch_and_extract_plant_data,
#                            range(TOTAL_NUMBER_OF_PLANTS + 1))

#     for plant_data in results:
#         if plant_data:
#             plant_dataframe = pd.concat(
#                 [plant_dataframe, pd.DataFrame([plant_data])], ignore_index=True)

#     return plant_dataframe

def load_into_dataframe() -> pd.DataFrame:
    """Fetches API data for all plants appends it to a DataFrame."""
    plant_dataframe = initialise_dataframe()
    for plant_id in range(TOTAL_NUMBER_OF_PLANTS + 1):
        plant_data = fetch_and_extract_plant_data(plant_id)
        if plant_data:
            plant_dataframe = pd.concat(
                [plant_dataframe, pd.DataFrame([plant_data])], ignore_index=True)

    return plant_dataframe


if __name__ == "__main__":
    print(load_into_dataframe())
