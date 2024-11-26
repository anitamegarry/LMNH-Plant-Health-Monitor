"""Connects to Microsoft SQL Server, extracts all data and stores it as a .csv file"""

# pylint: disable=E1101

import os
import csv

import pymssql
from dotenv import load_dotenv
import boto3
from datetime import datetime

load_dotenv()

SCHEMA = os.getenv("SCHEMA_NAME")

QUERY = f"""
SELECT
    recording.recording_id,
    recording.recording_taken,
    recording.last_watered,
    recording.soil_moisture,
    recording.temperature,
    plant.plant_id,
    species.plant_name,
    country.country_name,
    botanist.botanist_first_name,
    botanist.botanist_last_name,
    botanist.botanist_email,
    botanist.botanist_phone_number
FROM
    {SCHEMA}.recording
JOIN
    {SCHEMA}.plant ON recording.plant_id = plant.plant_id
JOIN
    {SCHEMA}.species ON plant.species_id = species.species_id
JOIN
    {SCHEMA}.country ON plant.country_id = country.country_id
JOIN
    {SCHEMA}.botanist ON plant.botanist_id = botanist.botanist_id;
"""

CSV_FILE = f"{datetime.today().strftime('%Y-%m-%d')}_plant_monitor_data.csv"


def get_connection():
    """Gets connection to Microsoft SQL server"""
    return pymssql.connect(database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USER"),
                           server=os.getenv("DB_HOST"),
                           password=os.getenv("DB_PASSWORD"))


def get_cursor(conn):
    """Gets cursor"""
    return conn.cursor()


def extract_data() -> None:
    """Extracts all data from database"""
    conn = get_connection()
    if not conn:
        return None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(QUERY)
        results = cursor.fetchall()
        column_titles = [description[0] for description in cursor.description]
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_titles)
            writer.writerows(results)
        print("Data extracted successfully.")
    except pymssql.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()
        print("Connection closed.")


def get_client():
    """Returns S3 client"""
    access_key_id = os.getenv("access_key_ID")
    secret_access_key = os.getenv("secret_access_key")
    client = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    return client


if __name__ == "__main__":
    print(get_connection())
    print(extract_data())