"""
The file responsible for hosting the dashboard where users can
see live plant status data ad access historical data 
"""

# pylint: disable=E1101
# pylint: disable=R0801

import os
from datetime import datetime, time, date
import pymssql
from dotenv import load_dotenv
import boto3
import botocore.exceptions
import altair as alt
import streamlit as st
import pandas as pd

load_dotenv()


def get_connection() -> None:
    """Gets connection to Microsoft SQL server"""
    return pymssql.connect(database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USER"),
                           server=os.getenv("DB_HOST"),
                           password=os.getenv("DB_PASSWORD"))


def setup_filters() -> None:
    """Creates the time and plant filters and displays them to the dashboard"""
    start_time = st.time_input("Start Time", value=None)
    end_time = st.time_input("End Time", value=None)

    plant_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    selected_plants = st.multiselect(
        "Selected Plant IDs", plant_ids, default=0)

    return start_time, end_time, selected_plants


def load_filtered_data(start_time: time, end_time: time, selected: list[int]) -> pd.DataFrame:
    """
    Filter the live data according to the time range and
    plant choices made by the user
    """
    schema = os.getenv("SCHEMA_NAME")

    if start_time is None:
        start_time = time(0, 0, 0)
    if end_time is None:
        end_time = time(23, 59, 59)
    if len(selected) == 1:
        selected = (selected[0], selected[0])
    if len(selected) == 0:
        selected = (-1, -1)

    query = f"""
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
        botanist.botanist_last_name
    FROM {schema}.recording
    JOIN {schema}.plant ON recording.plant_id = plant.plant_id
    JOIN {schema}.species ON plant.species_id = species.species_id
    JOIN {schema}.country ON plant.country_id = country.country_id
    JOIN {schema}.botanist ON plant.botanist_id = botanist.botanist_id
    WHERE CONVERT(TIME, recording.recording_taken) > '{start_time}'
    AND CONVERT(TIME, recording.recording_taken) < '{end_time}'
    AND plant.plant_id IN {tuple(selected)};
    """

    conn = get_connection()
    if not conn:
        return None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()
        filtered_data = pd.DataFrame(result)

        column_titles = [description[0]
                         for description in cursor.description]

        if not filtered_data.empty:
            filtered_data.columns = column_titles
            filtered_data['recording_taken'] = pd.to_datetime(
                filtered_data['recording_taken'])
        else:
            filtered_data = pd.DataFrame(column_titles)

        return filtered_data

    except pymssql.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()


def generate_soil_moisture_time_chart(plant_data: pd.DataFrame) -> alt.Chart:
    """Generates a soil moisture over time line graph"""
    soil_moisture_plot = alt.Chart(plant_data).mark_line().encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(title='Time of Recording')),
        y=alt.Y('soil_moisture:Q', axis=alt.Axis(title='Soil Moisture (%)')),
        color=alt.Color('plant_id:N', legend=alt.Legend(title='Plant ID'))
    ).properties(
        title="Soil Moisture Over Time"
    )

    return soil_moisture_plot


def generate_temperature_time_chart(plant_data: pd.DataFrame) -> alt.Chart:
    """Generates a temperature over time line graph"""
    temperature_plot = alt.Chart(plant_data).mark_line().encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(title='Time of Recording')),
        y=alt.Y('temperature:Q', axis=alt.Axis(title='Temperature (°C)')),
        color=alt.Color('plant_id:N', legend=alt.Legend(title='Plant ID'))
    ).properties(
        title="Temperature Over Time"
    )

    return temperature_plot


def display_title(title) -> None:
    """Displays the given text as the title of the dashboard"""
    st.title(title)


def display_plots(chart1: alt.Chart, chart2: alt.Chart) -> None:
    """Displays all the plots to our dashboard"""
    st.altair_chart(chart1, use_container_width=True)
    st.altair_chart(chart2, use_container_width=True)


def download_from_s3(file_name):
    """Download the given file from the long term S3 storage"""
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")
    s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
                      )
    try:
        s3.download_file("c14-plant-practitioners-long-term-storage",
                         file_name, file_name)
        return file_name
    except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ClientError) as e:
        print("boto3 error: ", e)
        return None


def display_historic_download_title() -> None:
    """Display the title for the historic data download section"""
    st.title("Download Historic Plant Data")


def create_download_button(date_range: list[date]) -> None:
    """Creates the logic and button for downloading historical data"""
    if len(date_range) == 2:
        if date_range[0] == date_range[1]:
            date_list = [date_range[0]]
        else:
            date_list = pd.date_range(start=date_range[0], end=date_range[1])
    elif len(date_range) == 1:
        date_list = [date_range[0]]
    else:
        return None

    formatted_dates = [date.strftime(
        '%Y-%m-%d') + '_plant_monitor_data.csv' for date in date_list]

    if 'date_files' not in st.session_state:
        st.session_state.date_files = []

    if st.button("Prepare Download"):
        st.session_state.date_files = formatted_dates

    if st.session_state.date_files:
        with st.spinner("Preparing file(s) for download..."):
            for file_formatted in st.session_state.date_files:
                file_name = os.path.basename(file_formatted)
                result = download_from_s3(file_name)
                if result is not None:
                    with open(file_name, "rb") as file:
                        st.download_button(
                            label=f"Click to Download {file_name}",
                            data=file,
                            file_name=file_name,
                            mime="text/csv"
                        )
    return None


def create_date_range_selector() -> list[date]:
    """Creates and displays the date range selector for downloading historic data"""
    today = datetime.now()

    start = date(2024, 1, 1)
    end = today

    date_range = st.date_input(
        "Select the range of dates you want to download historic data for",
        (date(today.year, today.month, today.day - 2),
         date(today.year, today.month, today.day - 1)),
        start,
        end,
        format="DD.MM.YYYY",
    )

    return date_range


def main():
    """The main logic of the dashboard"""
    display_title("LHNH PLant Monitoring Dashboard")
    start, end, selected_plants = setup_filters()
    plant_data = load_filtered_data(start, end, selected_plants)
    plot1 = generate_soil_moisture_time_chart(plant_data)
    plot2 = generate_temperature_time_chart(plant_data)
    display_plots(plot1, plot2)
    display_historic_download_title()
    dates_range = create_date_range_selector()
    create_download_button(dates_range)


if __name__ == "__main__":
    main()
