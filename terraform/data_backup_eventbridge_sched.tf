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
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c14_plant_practitioners_data_backup_ecr@sha256:f27ba26b68436c1b01f7940ed1dabb8ceec86f09c3db791687ba30d3f286f755"
}

resource "aws_cloudwatch_event_rule" "c14_plant_practitioners_backup_rule" {
  name                = "c14_plant_practitioners_backup_rule"
  description         = "trigger the lambda every 24 hours"
  schedule_expression = "cron(0 0 * * ? *)"

}

resource "aws_cloudwatch_event_target" "c14_plant_practitioners_backup_target" {
  rule      = aws_cloudwatch_event_rule.c14_plant_practitioners_backup_rule.name
  arn       = aws_lambda_function.c14_plant_practitioners_backup_lambda_function.arn
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