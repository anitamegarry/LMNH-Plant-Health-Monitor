resource "aws_iam_role" "c14_plant_practitioners_backup_lambda_role" {
  name = "c14_plant_practitioners_backup_lambda_role"
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

resource "aws_lambda_function" "c14_plant_practitioners_backup_lambda_function" {
  function_name = "c14_plant_practitioners_backup_lambda"
  role          = aws_iam_role.c14_plant_practitioners_backup_lambda_role.arn
  package_type  = "Image"
  image_uri     = "[DOCKER IMAGE URI HERE]"
  vpc_config {
    subnet_ids         = ["subnet-0497831b67192adc2", "subnet-0acda1bd2efbf3922", "subnet-0465f224c7432a02e"]  
    security_group_ids = [aws_security_group.c14_plant_practitioners_security_group.id]
  }
}

resource "aws_cloudwatch_event_rule" "c14_plant_practitioners_backup_rule" {
  name                = "c14_plant_practitioners_backup_rule"
  description         = "trigger the lambda every 24 hours"
  schedule_expression = "cron(0 0 * * ? *)"

}

resource "aws_cloudwatch_event_target" "c14_plant_practitioners_backup_target" {
  rule      = aws_cloudwatch_event_rule.c14_plant_practitioners_backup_rule.name
  arn       = aws_lambda_function.c14_plant_practitioners_backup_lambda_function.arn
  role_arn  = aws_iam_role.c14_plant_practitioners_backup_lambda_role.arn
}

resource "aws_lambda_permission" "c14_plant_practitioners_backup_lambda_permission" {
  statement_id  = "AllowEventBridgeInvokeDataBackup"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.c14_plant_practitioners_backup_lambda_function.function_name
  source_arn    = aws_cloudwatch_event_rule.c14_plant_practitioners_backup_rule.arn
}

resource "aws_iam_policy" "c14_plant_practitioners_backup_policy" {
  name        = "c14_plant_practitioners_backup_policy"
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

resource "aws_iam_role_policy_attachment" "c14_plant_practitioners_backup_policy_attachment" {
  role       = aws_iam_role.c14_plant_practitioners_backup_lambda_role.name
  policy_arn = aws_iam_policy.c14_plant_practitioners_backup_policy.arn
}