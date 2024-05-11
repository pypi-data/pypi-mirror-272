# infra -----------------------------------------------
data "aws_vpc" "default" {
  default = true
}

data "aws_vpc" "main" {
  count = var.vpc_name == "" ? 0:1
  tags = {
    Name = var.cluster_name
  }
}

data "aws_security_group" "host" {
  count = var.requires_compatibilities [0] != "EXTERNAL" ? 1: 0
  name = "${var.cluster_name}-member"
}

data "aws_alb" "load_balancer" {
  count = var.requires_compatibilities [0] != "EXTERNAL" ? 1: 0
  name = var.cluster_name
}

data "aws_subnets" "subnets" {
  count = var.requires_compatibilities [0] != "EXTERNAL" ? 1: 0
  filter {
    name   = "vpc-id"
    values = [data.aws_security_group.host [0].vpc_id]
  }
}

data "aws_iam_role" "ecs_tasks_execution_role" {
  name = "ecs-task-execution-role-${var.cluster_name}"
}

data "aws_iam_instance_profile" "profile" {
  count = var.requires_compatibilities [0] != "EXTERNAL" ? 1: 0
  name = "${var.cluster_name}-profile"
}

data "aws_iam_role" "ecs_service_role" {
  name = "ecs-service-role-${var.cluster_name}"
}

data "aws_iam_role" "ecs_task_role" {
  name = "ecs-task-role-${var.cluster_name}"
}

data "aws_ecs_cluster" "main" {
  cluster_name = var.cluster_name
}

data "aws_alb_listener" "front_end" {
  count             = length (data.aws_alb.load_balancer) > 0 ? 1 : 0
  load_balancer_arn = data.aws_alb.load_balancer [0].arn
  port              = 443
}

data "aws_launch_template" "host" {
  count = var.requires_compatibilities [0] != "EXTERNAL" ? 1: 0
  name = var.cluster_name
}

data "aws_iam_role" "ecs_service_autoscale_role" {
  name = "ecs-service-scale-application-${var.cluster_name}"
}
