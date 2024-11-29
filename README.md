# LMNH Plant Health Monitor

## Table of Contents

- [LMNH Plant Health Monitor](#lmnh-plant-health-monitor)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Diagrams](#diagrams)
    - [Database ERD:](#database-erd)
    - [AWS Architecture Diagram](#aws-architecture-diagram)
  - [Contributions](#contributions)
    - [Guidelines](#guidelines)
  - [Acknowledgements](#acknowledgements)

## Overview

This project automates the process of extracting, transforming, and loading (ETL) plant data from an external API into a cloud-based environment, hosted entirely on AWS. It is designed for the Liverpool Museum of Natural History to efficiently manage real-time plant data and ensure secure, long-term data storage.

The system extracts plant data every minute, loads it into an AWS RDS database for immediate analysis, and automates daily archival to AWS S3. Museum staff can access both real-time and historical data via an interactive Streamlit dashboard. By leveraging AWS services such as RDS, ECS, Lambda, and S3, the project provides a scalable, efficient, and secure solution to manage large volumes of plant data with minimal manual intervention.

## Features

1. Real-Time Data Processing

Real-time analysis of plant data is performed using an ECS-hosted dashboard, ensuring up-to-date insights for users.

2. ETL Pipeline for Data Transformation

A Lambda function runs every minute to extract, transform, and load (ETL) plant data into an RDS for short-term storage.

3. Integrated Docker Workflow

Docker images for ECS tasks are built and uploaded to ECR for easy deployment and management.

4. User-Friendly Dashboard

A Streamlit-based dashboard hosted on ECS allows users to view real-time and historical data through an intuitive interface.

## Technologies

Technologies used within this project include:
- AWS 
  - S3
  - RDS
  - ECR
  - ECS
  - Lambda
  - EventBridge
- Docker
- Microsoft SQL Server
- Python
- Terraform 

## Diagrams

### Database ERD:

![Database ERD](images/ERD.png)


### AWS Architecture Diagram

![AWS Architecture Diagram](images/architecture_diagram.png)

## Contributions

We welcome contributions to make this project better! If you have an idea, find a bug, or want to add a feature, follow these steps:

1. Fork the Repository
   
Create a personal copy of the repository by clicking the "Fork" button in GitHub.

2. Clone the Repository

Copy the repository to your local machine using the following command:

```git clone https://github.com/anitamegarry/LMNH-Plant-Health-Monitor.git```

3. Create a Branch
   
Create a branch for your changes with a descriptive name:

```git checkout -b feature/your-feature-name```

4. Make Your Changes
   
Implement your feature or fix the bug. Make sure to:

Follow the coding style guidelines (if any are defined).
Add or update documentation, if needed.
Write tests to cover any new functionality or changes.

5. Commit Your Changes
   
Commit your changes with a clear and concise commit message:

```git commit -m "Add a brief description of your changes"```

6. Push Your Branch
   
Push your changes to your forked repository:

```git push origin feature/your-feature-name```

7. Open a Pull Request
   
Go to the original repository on GitHub and open a Pull Request (PR):

Include a description of the changes you've made.
Mention any related issues (e.g., "Fixes #123").
Add screenshots or examples, if applicable.

8. Review Process
   
The maintainers will review your PR and may suggest changes. 
Once approved, your changes will be merged into the main project!


### Guidelines
To ensure a smooth contribution process, please follow these guidelines:

Use clear and descriptive commit messages.
Adhere to the project's coding standards and conventions.
Check for existing issues before opening a new one.
Be respectful and constructive in discussions.

## Acknowledgements

1. Project Contributors
   - [Jiulian Gutierrez](https://github.com/jiuliangut)
   - [Anita Megarry](https://github.com/anitamegarry)
   - [Fahad Rahman](https://github.com/Fahi28)
   - [Ben Trzcinski](https://github.com/bentrzcinski)

2. Open Source Libraries
   - **Open Source Libraries**: This project relies on several open-source libraries, including:
     - [pandas](https://pandas.pydata.org/) – A powerful data analysis and manipulation library for handling and analyzing plant data.
     - [boto3](https://boto3.amazonaws.com/) - The AWS SDK for Python, used for interacting with AWS services such as S3, RDS, and Lambda.
     - [requests](https://requests.readthedocs.io/en/latest/) - A simple and elegant HTTP library for Python, used for making API calls.
     - [pytest](https://docs.pytest.org/en/stable/) – A testing framework for Python, used for running unit tests in this project.
     - [pymssql](https://pymssql.readthedocs.io/en/latest/) - A Python library for connecting to Microsoft SQL Server, used to interact with the RDS database.

