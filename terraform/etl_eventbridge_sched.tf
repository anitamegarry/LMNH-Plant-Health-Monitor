# define iam role
resource "aws_iam_role" "c14_plant_practitioners_etl_lambda_role" {
  name = "c14_plant_practitioners_etl_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Action   = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# define lambda function
resource "aws_lambda_function" "c14_plant_practitioners_etl_lambda_function" {
  function_name = "c14_plant_practitioners_etl_lambda"
  role          = aws_iam_role.c14_plant_practitioners_etl_lambda_role.arn
  package_type  = "Image"
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c14_plant_practitioners_etl_ecr@sha256:ca7d0ffe14ffb7bab95a71ffc249c11b107fd3bbdd56f8ae18fc8d2e32d03769"
  environment {
    variables = {
      DB_HOST            = var.db_host
      DB_PORT            = var.db_port
      DB_PASSWORD        = var.db_password
      DB_USER            = var.db_user
      DB_NAME            = var.db_name
      SCHEMA_NAME        = var.schema_name
    }
  }
}

# create cloudwatch event rule - schedule for the event
resource "aws_cloudwatch_event_rule" "c14_plant_practitioners_etl_rule" {
  name                = "c14_plant_practitioners_etl_rule"
  description         = "trigger the lambda every minute"
  schedule_expression = "cron(0/1 * * * ? *)"
}

# eventbridge target for lambda
resource "aws_cloudwatch_event_target" "c14_plant_practitioners_etl_target" {
  rule      = aws_cloudwatch_event_rule.c14_plant_practitioners_etl_rule.name
  arn       = aws_lambda_function.c14_plant_practitioners_etl_lambda_function.arn
}

# lambda permission - allows eventbridge to trigger lambda
resource "aws_lambda_permission" "c14_plant_practitioners_etl_lambda_permission" {
  statement_id  = "AllowEventBridgeInvokeETL"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.c14_plant_practitioners_etl_lambda_function.function_name
  source_arn    = aws_cloudwatch_event_rule.c14_plant_practitioners_etl_rule.arn
}

# policy to define permissions
resource "aws_iam_policy" "c14_plant_practitioners_etl_policy" {
  name        = "c14_plant_practitioners_etl_policy"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject", "ecs:RunTask"]
        Resource = "*"
      }
    ]
  })
}

# attach policy to iam role
resource "aws_iam_role_policy_attachment" "c14_plant_practitioners_etl_policy_attachment" {
  role       = aws_iam_role.c14_plant_practitioners_etl_lambda_role.name
  policy_arn = aws_iam_policy.c14_plant_practitioners_etl_policy.arn
}