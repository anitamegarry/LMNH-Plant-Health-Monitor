
# LMNH Plant Monitoring Dashboard

The LHNH Plant Monitoring Dashboard is a web-based application that allows users to visualize live plant status data, apply custom filters, and access historical plant data stored in an Amazon S3 bucket. The dashboard is built using Streamlit for visualization and Altair for interactive charts, and integrates with an RDS database for live data and AWS S3 for long-term storage.

## Features

1. Live Data Visualization
- Filter plant data by time range and specific plant IDs.
- View interactive line charts for:
  - Soil Moisture Over Time
  - Temperature Over Time
  
2. Historical Data Access
- Select date ranges to prepare and download historical plant monitoring data.
- Download data in CSV format directly from Amazon S3.


## Prerequisites
1. Environment Variables
   
The application uses a ```.env``` file to manage sensitive credentials. Ensure the following variables are set:

- ```DB_NAME```: Name of the RDS database
- ```DB_USER```: Database username
- ```DB_HOST```: Database host address
- ```DB_PASSWORD```: Database password
- ```SCHEMA_NAME```: Schema name for the database tables
- ```BUCKET_NAME```: Name of the S3 bucket storing historical data files

2. Python Libraries
 
Install the required libraries with:

```pip install -r requirements.txt```

3. AWS Credentials
 
Ensure your system or application has proper AWS credentials set up for accessing the S3 bucket.

## Usage

Dashboard Features
- Live Data Filters
  - Set a start time and end time for the data filter.
  - Select specific Plant IDs to focus on.
  
- Live Charts
  - Soil Moisture Over Time: Shows moisture percentage over time.
  - Temperature Over Time: Displays temperature trends for selected plants.
  
- Historical Data Download
  - Select a date range for historical data.
  - Click Prepare Download to fetch available data files from S3.
  - Download prepared files directly from the dashboard.

## AWS S3 Integration
The dashboard integrates with Amazon S3 to fetch historical plant data:

Files are stored in the format: ```YYYY-MM-DD_plant_monitor_data.csv```
Download logic ensures the correct file is retrieved based on user input.

## Design Decisions Made
As we have decided to retain extreme values within the database in case the museum staff wants to use it for troubleshooting, for the SQL queries for the graph, we have decided to exclude these extreme values so that the graphs are more useful to the staff for statistical analysis.