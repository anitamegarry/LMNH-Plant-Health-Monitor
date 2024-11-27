# LMNH Plant Health Monitor

### Database ERD:

![Database ERD](images/ERD.png)


### AWS Architecture Diagram

![AWS Architecture Diagram](images/architecture_diagram.png)


### Terraform Configuration:
The `terraform` folder contains all files for terraform infrastructure:
- `provider.tf` - defines the AWS region.
- `s3_bucket.tf` - provisioning the AWS S3 bucket for long-term data storage (data older than 24hrs).
  
One script for each of the 3 ECRs utilised in this project:
- `dashboard_ecr.tf`
- `etl_ecr.tf`
- `data_backup_ecr.tf`
- Each ECR has a lifecycle policy which keeps only the 30 most recently pushed images.