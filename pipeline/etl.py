"""Script that emulates the ETL pipeline in a single file."""
import load


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """Calls load.main() when the Lambda is invoked on AWS"""
    try:
        load.main()
        return {"statusCode": 200, "body": "Successfully executed ETL pipeline"}
    except Exception as e:  # pylint: disable=broad-except
        return {"statusCode": 500, "body": f"Error occurred: {str(e)}"}
