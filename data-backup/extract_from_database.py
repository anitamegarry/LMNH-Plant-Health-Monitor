"""Connects to Microsoft SQL Server, extracts all data,
stores it as a .csv file, uploads to S3 and resets the database"""

# pylint: disable=E1101
# pylint: disable=W0613
# pylint: disable=E1120

import os
import csv
from datetime import datetime

import pymssql
from dotenv import load_dotenv
import boto3

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

CSV_FILE = f"""/tmp/{datetime.today().strftime('%Y-%m-%d')
                     }_plant_monitor_data.csv"""


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
        return None
    except pymssql.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()
        print("Connection closed.")


def get_client():
    """Returns S3 client"""
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")
    client = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    return client


def truncate_table():
    """Truncates tables within the schema"""
    conn = get_connection()
    if not conn:
        return None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(f"TRUNCATE TABLE {SCHEMA}.recording")
        print("Table truncated.")
        conn.commit()
        return None
    except pymssql.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()
        print("Connection closed.")


def lambda_handler(event, context):
    """Lambda function that runs the data backup pipeline"""
    try:
        extract_data()
        s3_client = get_client()
        s3_client.upload_file(CSV_FILE, os.getenv("BUCKET_NAME"), CSV_FILE)
        truncate_table()
        return {"statusCode": 200, "body": "Successfully executed data backup pipeline"}
    except Exception as e:  # pylint: disable=broad-except
        return {"statusCode": 500, "body": f"Error occurred: {str(e)}"}


if __name__ == "__main__":
    extract_data()
    s3 = get_client()
    s3.upload_file(CSV_FILE, os.getenv("BUCKET_NAME"), CSV_FILE)
    truncate_table()
