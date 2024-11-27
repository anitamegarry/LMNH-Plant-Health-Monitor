# Pipeline
This folder contains all the scripts required to execute our ETL pipeline, and convert it into a docker image ready to be uploaded to an AWS ECR.

### Requirements
You need to install all the required libraries before you can execute the pipeline scripts. To do this run:
 - pip3 install -r requirements.txt

### Execution
To run the pipeline within a local environment, execute the etl.py script with the following command:
 - python3 etl.py

To convert the pipeline script into a dockerised container, ready to upload to an AWS ECR, run the following command **from the root project directory**:
 - docker build -t [image name] -f pipeline/dockerfile --platform "linux/amd64" .