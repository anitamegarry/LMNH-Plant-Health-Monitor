"""
The file responsible for hosting the dashboard where users can
see live plant status data ad access historical data
"""

import altair as alt
import streamlit as st
import pandas as pd
from extract import download_truck_data_files, collate_data, clean_data, tidy_up
from pipeline import db_connect, db_close
from dotenv import load_dotenv
from os import environ as ENV


def display_title() -> None:
    st.title("T3 Truck Data Dashboard")


def filter_data(truck_data: pd.DataFrame):
    """
    Filter the data according to the date range and
    truck choices made by the user
    """
    start_date = st.date_input("Start Date", truck_data['timestamp'].min())
    end_date = st.date_input("End Date", truck_data['timestamp'].max())

    unique_trucks = sorted(truck_data['truck_id'].unique())
    selected_trucks = st.multiselect(
        "Selected Truck IDs", unique_trucks, default=unique_trucks)

    filtered_data = truck_data[
        (truck_data['timestamp'] >= pd.to_datetime(start_date)) &
        (truck_data['timestamp'] <= pd.to_datetime(end_date)) &
        (truck_data['truck_id'].isin(selected_trucks))
    ]

    return filtered_data


def load_local_data() -> pd.DataFrame:
    """Loads all the truck data into a pandas dataframe"""
    # Getting the truck data csv from the S3
    download_truck_data_files()
    collate_data()
    clean_data()
    tidy_up()

    # Loading it into a pandas df
    truck_data = pd.read_csv("data/historical_truck_data.csv")

    # Cleaning it up a bit
    truck_data['timestamp'] = pd.to_datetime(truck_data['timestamp'])

    return truck_data


def generate_transaction_count_time_chart(truck_data: pd.DataFrame) -> alt.Chart:
    """Generates a transaction count over time bar graph"""
    transaction_count_time = filtered_data.groupby(
        truck_data['timestamp'].dt.date).size().reset_index(name='count')

    transaction_count_time_chart = alt.Chart(transaction_count_time).mark_bar(color='#006666', size=30).encode(
        alt.Y('count:Q').title('Number of Transactions'),
        alt.X('timestamp:T', title='Date', axis=alt.Axis(format='%b %d'))
    ).properties(title="Transaction Count Over Time")

    return transaction_count_time_chart


def generate_transaction_value_time_chart(truck_data: pd.DataFrame) -> alt.Chart:
    """Generates a transaction value over time area plot"""
    transaction_value_time = truck_data.groupby(truck_data['timestamp'].dt.date)[
        'total'].sum().reset_index(name='total_value')

    transaction_value_time_chart = alt.Chart(transaction_value_time).mark_area(interpolate='linear', color='#006666').encode(
        x=alt.X('timestamp:T', title='Date', axis=alt.Axis(format='%b %d')),
        y=alt.Y('total_value:Q', title='Total Transaction Value')
    ).properties(title="Total Transaction Value Over Time")

    return transaction_value_time_chart


def generate_card_vs_cash_chart(truck_data: pd.DataFrame) -> alt.Chart:
    """Generates a total card vs total cash transactions pie chart"""
    card_vs_cash = truck_data.groupby(
        "type")["type"].count().reset_index(name='value')

    card_vs_cash_chart = alt.Chart(card_vs_cash).mark_arc().encode(
        theta=alt.Theta(field='value', type='quantitative'),
        color=alt.Color(field='type', type='nominal', title="Type",
                        scale=alt.Scale(range=['#004C4C', '#66B2B2']))
    ).properties(title="Total Transactions (Cash vs Card)")

    card_vs_cash_labels = card_vs_cash_chart.mark_text(radius=50, fill='white', fontSize=16).encode(
        theta=alt.Theta(field='value', type='quantitative', stack=True),
        text=alt.Text('value:Q')
    )

    card_vs_cash_combined = alt.layer(card_vs_cash_chart, card_vs_cash_labels)

    return card_vs_cash_combined


def generate_card_reader_chart(truck_data: pd.DataFrame) -> alt.Chart:
    """Generates a pie chart showing what percentage of trucks have card readers"""
    # Graph 4 (TEMPORARILY UNAVAILABLE WHILE USING LOCAL CSV)
    card_machines = truck_data.groupby(
        "type")["type"].count().reset_index(name='value')

    card_machines_chart = alt.Chart(card_machines).mark_arc().encode(
        theta=alt.Theta(field='value', type='quantitative'),
        color=alt.Color(field='type', type='nominal', title="Type",
                        scale=alt.Scale(range=['#004C4C', '#66B2B2']))
    ).properties(title="Total Transactions (Cash vs Card)")

    card_machines_labels = card_machines_chart.mark_text(radius=50, fill='white', fontSize=16).encode(
        theta=alt.Theta(field='value', type='quantitative', stack=True),
        text=alt.Text('value:Q')
    )

    card_machines_combined = alt.layer(
        card_machines_chart, card_machines_labels)

    return card_machines_combined


def display_plots(chart1: alt.Chart, chart2: alt.Chart, chart3: alt.Chart, chart4: alt.Chart) -> None:
    """Displays all the plots to our dashboard"""
    col1, col2, col3 = st.columns([0.55, 0.1, 0.35])
    with col1:
        st.altair_chart(chart1, use_container_width=True)
    with col3:
        st.altair_chart(chart2, use_container_width=True)

    col1, col2, col3 = st.columns([0.35, 0.1, 0.55])
    with col1:
        st.altair_chart(chart3, use_container_width=True)
    with col3:
        st.altair_chart(chart4, use_container_width=True)


if __name__ == "__main__":
    display_title()
    data = load_local_data()
    filtered_data = filter_data(data)
    plot1 = generate_transaction_count_time_chart(filtered_data)
    plot2 = generate_card_vs_cash_chart(filtered_data)
    plot3 = generate_card_reader_chart(filtered_data)
    plot4 = generate_transaction_value_time_chart(filtered_data)
    display_plots(plot1, plot2, plot3, plot4)
