# Terraform Infrastructure

This folder contains the Terraform scripts necessary to provision the AWS infrastructure for the ETL pipeline, the data backup script, and the streamlit dashboard.

### Architecture Decisions
- AWS Lambda was chosen to run both the ETL and the backup pipeline for cost-efficiency. Since these are relatively short tasks and cost is only accrued when the Lambda is running, this should keep costs down. Lambda was ultimately chosen over a Fargate for simpler management of scalability.
- The Streamlit dashboard for visualisation is deployed as an ECS service to ensure it runs constantly, allowing users to access the dashboard at any given time. ECS can also be auto-scaled to allow handling of changes in user traffic.
- An AWS S3 Bucket was chosen for long-term storage of data older than 24 hours. Though slightly more expensive than other long-term storage services such as Glacier, it is more cost-effective given that the users may need periodic access to the data - S3 allows this without incurring extra costs.


### Prerequisites
Before running the Terraform scripts, make sure you have Terraform installed. You also need to configure your AWS credentials. 

To install Terraform, run: `brew install terraform`

### Execution
To deploy the infrastructure, run the following Terraform commands from the root project directory:

1. Initialise Terraform: `terraform init`
2. Plan the infrastucture: `terraform plan`
3. Apply the plan and provision resources: `terraform apply`


### These terraform files implement the following AWS resources:

- **`s3_bucket.tf`**
   - `c14-plant-practitioners-long-term-storage` - For long term storage of plant data files as CSVs
  
- **`etl_ecr.tf`**
  - `c14_plant_practitioners_etl_ecr` - ECR for hosting ETL docker image
  - `c14_plant_practitioners_etl_ecr_lifecycle_policy` - Lifecycle policy keeping only the 30 latest images pushed to the ECR
- **`etl_eventbridge_sched.tf`**
  - `c14_plant_practitioners_etl_lambda_role` - defines the iam role
  - `c14_plant_practitioners_etl_lambda_function` - defines the Lambda function
  - `c14_plant_practitioners_etl_rule` - defines the eventbridge rule (every minute)
  - `c14_plant_practitioners_etl_target` - defines the target for the eventbridge rule
  - `c14_plant_practitioners_etl_lambda_permission` - allows eventbridge to trigger the lambda function
  - `c14_plant_practitioners_etl_policy` - defines iam role persmissions
  - `c14_plant_practitioners_etl_policy_attachment` - attaches iam policy to role
  
- **`data_backup_ecr.tf`** 
  - `c14_plant_practitioners_data_backup_ecr` - ECR for hosting data backup script docker image
  - `c14_plant_practitioners_data_backup_ecr_lifecycle_policy` - Lifecycle policy keeping only the 30 latest images pushed to the ECR
  
- **`data_backup_eventbridge_sched.tf`**
  - This contains the same resource types as in `etl_eventbridge_sched.tf`, but are separate resource instances for handling the data backup script which is triggered every 24 hours.
- **`dashboard_ecr.tf`**
  - `c14_plant_practitioners_dashboard_ecr` - ECR for hosting streamlit dashboard docker image
- **`dashboard_ecs.tf`**
  - `c14_plant_practitioners_task_definition` - Task definition for dashboard code image
  - `c14_plant_practitioners_log_group` - Log group for monitoring task definition health
- **`ecs_security_group.tf`**
  - `c14_plant_practitioners_security_group` - security group currently allowing all inbound and outbound traffic 
- 
