"""Script that emulates the ETL pipeline in a single file."""
import load


def lambda_handler(event, context):
    """Calls load.main() when the Lambda is invoked on AWS"""
    try:
        load.main()
        return {"statusCode": 200, "body": "Successfully executed ETL pipeline"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error occurred: {str(e)}"}
