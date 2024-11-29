# Pipeline
This folder contains all the scripts required to execute our ETL pipeline, and convert it into a docker image ready to be uploaded to an AWS ECR.

### Requirements
You need to install all the required libraries before you can execute the pipeline scripts. To do this run:
 - pip install -r requirements.txt

### Execution
To run the pipeline within a local environment, execute the etl.py script with the following command:
 - python3.9 etl.py

To convert the pipeline script into a dockerised container, ready to upload to an AWS ECR, run the following command **from the root project directory**:
 - docker build -t [image name] -f pipeline/dockerfile --platform "linux/amd64" .


## Features of each Python script

### Extract

The Extract script is responsible for connecting to the ```data-eng-plants``` API, retrieving data about plants, and storing it in a pandas DataFrame. The script utilizes Python's ```requests``` library to perform GET requests for plant data, handling up to 50 plant records from the API.

#### Key Functions

- ```get_plant_data(plant_id: int)```: Sends a GET request to the API to retrieve data for a specific plant by its ID. Handles timeouts and errors gracefully.
- ```extract_plant_data(response: dict)```: Processes the API response to extract relevant fields, ensuring all fields are present, even if some data is missing or incomplete. Fields include:
  - Botanist's first and last names
  - Botanist's contact details (email, phone number)
  - Plant name (scientific or common)
  - Recording details (e.g., date, soil moisture, temperature)
  - Origin country code
  - Plant ID
- ```load_into_dataframe()```: Iteratively fetches and processes data for all plants and appends the extracted data into a pandas DataFrame. Missing or invalid records are ignored.

#### Design Decisions Made

With the data retrieved from the API being quite inconsistent, some plants having more information than others, the above fields mentioned were determined as the ones shared amongst all plants and those necessary for the museum staff to be able to make sense of and use the data. An example of this inconsistency is the ```plant_name```, all plants have some combination of common name and/or scientific name but there is no consistency there so we made the decision to prioritize the common name and if that is not available take the scientific name.  

With the GET request being an iterative process with a total of approximately 50 requests being made per run, the plan was to make use of Python's ```multiprocessing``` module to speed up the process, however due to limitations with AWS Lambda not supporting this feature, we made the decision to have it run as a single task with the trade off of the run time of the script being slower.

### Transform

The Transform script ensures that the extracted plant data adheres to the database schema and performs the following data cleaning and transformation steps:

#### Key Functions

- ```convert_columns_to_datetime(dataframe: pd.DataFrame)```: Converts the recording_taken and last_watered columns to datetime format. This function ensures:

  - Invalid or poorly formatted dates are coerced into NaT.
  - All datetime values are standardized to the UTC timezone, localizing them if no timezone is present or converting them if already localized.
  
- ```clean_name(name: str)```: Cleans individual names by:

  - Removing non-alphabetic characters (e.g., numbers, special characters).
  - Stripping extra spaces and converting the name to lowercase for consistency.
  
- ```clean_plant_names(dataframe: pd.DataFrame)```: 
Applies the clean_name function to the plant_name column, ensuring all plant names are cleaned and standardized.

- ```main()```: Orchestrates the transformation process by:

  - Loading the raw DataFrame using the ```load_into_dataframe``` function from the Extract script.
  - Converting date columns to a uniform datetime format.
  - Cleaning and standardizing plant names.

#### Design Decisions Made

Due to the ```initialise_dataframe``` function within the Extract script, there was not much cleaning that was needed to be done within this script. The few exceptions to this were to ensure that values within ```plant_name``` were in a lower case format with no leading/trailing white space so that they conformed with the schema. In addition to this, the columns ```recording_taken``` and ```last_watered``` were dates and times in a string format, so it was decided to ensure that these conformed to a standard datetime format that matched the schema.

Furthermore, there are extreme values present within the ```soil_moisture``` and ```temperature``` columns however we decided to keep these values within the database as these could be valuable to the museum staff for potential troubleshooting regarding the sensor system. Though we do understand that these extremes are not valuable for visualisation of the data and therefore will include filters within our streamlit dashboard that will exclude these extremes.


### Load

The Load script inserts the transformed plant data into an RDS instance. It ensures that data is mapped correctly to the database schema and maintains referential integrity by retrieving foreign keys.

#### Key Functions

- ```get_connection()```: Establishes a connection to the Microsoft SQL Server database using credentials stored in environment variables. These credentials are managed using the ```dotenv``` library.
  
- ```get_cursor(connection: object)```: Creates and returns a cursor object for executing SQL queries on the database.

- ```get_foreign_key(db_cursor: object, table_name: str, column_name: str, value: str)```: Retrieves the foreign key for a given value by querying the database. Ensures that all foreign key constraints are satisfied before inserting data into dependent tables. Raises an error if the value does not exist.

- ```get_all_plant_foreign_keys(db_cursor: object, dataframe: pd.DataFrame)```: Processes the plant data and retrieves foreign keys for each row in the DataFrame. It ensures consistency by querying relevant tables (e.g., botanist, species, country) and returning a list of tuples containing the required foreign key values.

- ```insert_into_recording_table(connection: object, db_cursor: object, dataframe: pd.DataFrame)```: Iterates over the transformed DataFrame and inserts the plant recording data into the recording table. Commits each insertion to ensure data persistence.

- ```main()```: Orchestrates the loading process by:

  - Loading environment variables for database credentials.
  - Loading and transforming the plant DataFrame using the Transform script.
  - Establishing a database connection and retrieving a cursor.
  - Inserting the cleaned and transformed data into the database.

#### Design Decisions Made

Since the data being collated from the API is constantly about the same plants with only a few keys changing, it was decided for 4 out of the 5 tables in the schema to be seeded using the data from the DataFrame created in the Extract script. Due to this there is only 1 table, ```recording```, which was left to be filled. 

### ETL

This script collates the main functions from each separate function so that it can be run with a single command:

```python3.9 etl.py```