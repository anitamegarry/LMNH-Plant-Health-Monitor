# Data Backup

This folder contains all the scripts required to convert all the short term data in our Microsoft SQL Server Database to long term storage as a CSV file in our S3. It also contains the logic to clear the short term database afterwords to save on costs. 

### Requirements

You need to install all the required libraries before you can execute the data backup script. To do this run:

1. pip3 install -r requirements.txt

2. brew install sqlcmd

### Execution

To execute a data backup within a local environment, run the following command:

1. python3 extract_from_database.py


### Dockerisation

A docker image can be created with `dockerfile`. On activation, this will install all the requirements and run the `extract_from_database.py` file in a controlled environment.

To create and test the Docker image locally, follow these steps:

1. Build the Docker image:

docker build -t data-backup-local --platform "linux/amd64" .

2. Run the Docker container:

docker run -p 9000:8080 --env-file .env data-backup-local

3. Test the container:

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

To run the image on AWS:

Follow the push instructions on your AWS ECR repository, ensuring the tag --platform "linux/amd64" is used.
