data "aws_security_group" "c14_plant_practitioners_security_group" {
  name        = "c14_plant_practitioners_security_group"
}

data "aws_ecr_repository" "c14_plant_practitioners_dashboard_ecr" {
  name                 = "c14_plant_practitioners_dashboard_ecr"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

data "aws_ecs_cluster" "c14-ecs-cluster" {
  cluster_name = "c14-ecs-cluster"
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
        image     = "${data.aws_ecr_repository.c14_plant_practitioners_dashboard_ecr.repository_url}:latest"
        cpu       = 256
        memory    = 512
        essential = true
        environment = [
          { name = "DB_HOST", value = var.db_host },
          { name = "DB_PORT", value = var.db_port },
          { name = "DB_PASSWORD", value = var.db_password },
          { name = "DB_USER", value = var.db_user },
          { name = "DB_NAME", value = var.db_name },
          { name = "SCHEMA_NAME", value = var.schema_name },
          { name = "BUCKET_NAME", value = var.bucket_name },
          { name = "ACCESS_KEY_ID", value = var.access_key_id },
          { name = "SECRET_ACCESS_KEY", value = var.secret_access_key }
        ]
        portMappings = [
          {
            containerPort = 8501
            hostPort      = 8501
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
  cluster         = data.aws_ecs_cluster.c14-ecs-cluster.id  
  task_definition = aws_ecs_task_definition.c14_plant_practitioners_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = ["subnet-0497831b67192adc2", "subnet-0acda1bd2efbf3922", "subnet-0465f224c7432a02e"]
    security_groups  = [data.aws_security_group.c14_plant_practitioners_security_group.id]
    assign_public_ip = true
  }
}