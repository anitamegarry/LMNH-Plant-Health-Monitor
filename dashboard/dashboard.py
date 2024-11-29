"""
The file responsible for hosting the dashboard where users can
see live plant status data ad access historical data
"""

import altair as alt
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pymssql
from dotenv import load_dotenv
import boto3

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

    unique_plants = [1, 2, 3]
    selected_plants = st.multiselect(
        "Selected Plant IDs", unique_plants, default=unique_plants)


def load_filtered_data() -> pd.DataFrame:
    """
    Filter the live data according to the time range and
    plant choices made by the user
    """
    SCHEMA = os.getenv("SCHEMA_NAME")

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
    FROM {SCHEMA}.recording
    JOIN {SCHEMA}.plant ON recording.plant_id = plant.plant_id
    JOIN {SCHEMA}.species ON plant.species_id = species.species_id
    JOIN {SCHEMA}.country ON plant.country_id = country.country_id
    JOIN {SCHEMA}.botanist ON plant.botanist_id = botanist.botanist_id;
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

        column_titles = [description[0] for description in cursor.description]
        filtered_data.columns = column_titles
        filtered_data['recording_taken'] = pd.to_datetime(
            filtered_data['recording_taken'])

        return filtered_data

    except pymssql.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()


def generate_soil_moisture_time_chart(plant_data: pd.DataFrame) -> alt.Chart:
    """Generates a soil moisture over time line graph"""
    soil_moisture_plot = alt.Chart(plant_data).mark_line().encode(
        x='recording_taken:T',
        y='soil_moisture:Q',
        color='plant_id:N'
    ).properties(
        title="Soil Moisture Over Time"
    )

    return soil_moisture_plot


def generate_temperature_time_chart(truck_data: pd.DataFrame) -> alt.Chart:
    """Generates a temperature over time line graph"""
    temperature_plot = alt.Chart(plant_data).mark_line().encode(
        x='recording_taken:T',
        y='temperature:Q',
        color='plant_id:N'
    ).properties(
        title="Temperature Over Time"
    )

    return temperature_plot


def display_title(title) -> None:
    st.title(title)


def display_plots(chart1: alt.Chart, chart2: alt.Chart) -> None:
    """Displays all the plots to our dashboard"""
    col1, col2, col3 = st.columns([0.35, 0.1, 0.55])
    st.altair_chart(chart1, use_container_width=True)
    st.altair_chart(chart2, use_container_width=True)


if __name__ == "__main__":
    display_title("LHNH PLant Monitoring Dashboard")
    setup_filters()
    plant_data = load_filtered_data()
    plot1 = generate_soil_moisture_time_chart(plant_data)
    plot2 = generate_temperature_time_chart(plant_data)
    display_plots(plot1, plot2)
    print(plant_data["plant_id"])
