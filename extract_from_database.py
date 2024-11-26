"""Connects to Microsoft SQL Server, extracts all data and stores it as a .csv file"""

# pylint: disable=E1101

import os

import pymssql
from dotenv import load_dotenv
import boto3

load_dotenv()


def get_connection():
    """Gets connection to Microsoft SQL server"""
    return pymssql.connect(database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USER"),
                           server=os.getenv("DB_HOST"),
                           password=os.getenv("DB_PASSWORD"))


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
