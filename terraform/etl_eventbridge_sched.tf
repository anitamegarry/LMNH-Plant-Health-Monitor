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
  image_uri     = "[DOCKER IMAGE URI HERE]"
    vpc_config {
    subnet_ids         = ["subnet-0497831b67192adc2", "subnet-0acda1bd2efbf3922", "subnet-0465f224c7432a02e"]  
    security_group_ids = [aws_security_group.c14_plant_practitioners_security_group.id]
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
  role_arn  = aws_iam_role.c14_plant_practitioners_etl_lambda_role.arn
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