# pylint: disable=E1101
"""Script that will insert plant data into RDS."""
import os
from typing import List, Tuple
import pymssql
import pandas as pd
from dotenv import load_dotenv
import transform as tf


def get_connection() -> object:
    """Gets connection to Microsoft SQL server"""
    return pymssql.connect(database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USER"),
                           server=os.getenv("DB_HOST"),
                           password=os.getenv("DB_PASSWORD"))


def get_cursor(connection: object) -> object:
    """Gets cursor"""
    return connection.cursor()


def get_foreign_key(db_cursor: object, table_name: str,
                    column_name: str, value: str) -> int:
    """Gets foreign keys."""
    db_cursor.execute(
        f"SELECT * FROM {os.getenv('SCHEMA_NAME')}.{table_name} WHERE {column_name} = %s", (value,))
    result = db_cursor.fetchone()
    if result:
        return result[0]
    print(f"Querying {table_name} for {column_name} = {value}")
    raise ValueError('Invalid Data!')


def get_all_plant_foreign_keys(db_cursor: object,
                               dataframe: pd.DataFrame) -> List[Tuple[int, int, int]]:
    """Gets all foreign keys for the plant table,"""
    foreign_keys = []
    for index, row in dataframe.iterrows():
        try:
            botanist_id = get_foreign_key(
                db_cursor, 'botanist', 'botanist_email', row['botanist_email'])
            species_id = get_foreign_key(
                db_cursor, 'species', 'plant_name', row['plant_name'])
            country_id = get_foreign_key(
                db_cursor, 'country', 'country_code', row['country_code'])
            foreign_keys.append((botanist_id, species_id, country_id))
        except ValueError as e:
            print(f"Error processing row {index}, {e}")
    return foreign_keys


def insert_into_recording_table(connection: object,
                                db_cursor: object,
                                dataframe: pd.DataFrame) -> None:
    """Insert necessary data from DataFrame into the recording table."""
    for index, row in dataframe.iterrows():

        plant_id = row['plant_id']
        recording_taken = row['recording_taken']
        last_watered = row['last_watered']
        soil_moisture = row['soil_moisture']
        temperature = row['temperature']

        db_cursor.execute("""
                        INSERT INTO recording (plant_id, recording_taken, last_watered, soil_moisture, temperature) VALUES
                        (%s, %s, %s, %s, %s)""",
                          (plant_id, recording_taken, last_watered, soil_moisture, temperature))
        connection.commit()


def main() -> None:
    """Calls the above functions."""
    load_dotenv()
    plant_dataframe = tf.main()
    conn = get_connection()
    cursor = get_cursor(conn)
    insert_into_recording_table(conn, cursor, plant_dataframe)


if __name__ == "__main__":
    main()
