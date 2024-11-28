# Data Backup
This folder contains all the scripts required to convert all the short term data in our Microsoft SQL Server Database to long term storage as a CSV file in our S3. It also contains the logic to clear the short term database afterwords to save on costs. 

### Requirements
You need to install all the required libraries before you can execute the data backup script. To do this run:
 - pip3 install -r requirements.txt
 - brew install sqlcmd

### Execution
To execute a data backup within a local environment, run the store_data_longterm_and_reset_database.sh script with the following command:
 - sh store_data_longterm_and_reset_database.sh