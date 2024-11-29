data "aws_security_group" "c14_plant_practitioners_security_group" {
  name        = "c14_plant_practitioners_security_group"
}

data "aws_ecr_repository" "c14_plant_practitioners_dashboard_ecr" {
  name                 = "c14_plant_practitioners_dashboard_ecr"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

resource "aws_cloudwatch_log_group" "c14_plant_practitioners_log_group" {
  name              = "/ecs/c14_plant_practitioners_task_definition"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "c14_plant_practitioners_task_definition" {
  family                   = "c14_plant_practitioners_task_definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "c14-plant-practitioners-container"

      # Need to add ECR image to task def

      image     = "${aws_ecr_repository.plant_practitioners_repo.repository_url}:latest"  
      cpu       = 256
      memory    = 512
      essential = true
      environment = {
        variables = {
            DB_HOST            = var.db_host
            DB_PORT            = var.db_port
            DB_PASSWORD        = var.db_password
            DB_USER            = var.db_user
            DB_NAME            = var.db_name
            SCHEMA_NAME        = var.schema_name
            BUCKET_NAME        = var.bucket_name
            ACCESS_KEY_ID      = var.access_key_id
            SECRET_ACCESS_KEY  = var.secret_access_key
            }
        }
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.c14_plant_practitioners_log_group.name
          awslogs-region        = "eu-west-2"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
    execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
    task_role_arn      = data.aws_iam_role.ecs_task_execution_role.arn
}

resource "aws_ecs_service" "c14_plant_practitioners_service" {
  name            = "c14-plant-practitioners-service"
  cluster         = aws_ecs_cluster.c14-ecs-cluster.id
  task_definition = aws_ecs_task_definition.c14_plant_practitioners_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = ["subnet-0497831b67192adc2", "subnet-0acda1bd2efbf3922", "subnet-0465f224c7432a02e"]
    security_groups  = [data.aws_security_group.c14_plant_practitioners_security_group.id]
    assign_public_ip = true
  }
}