terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "h3lab-states-data"
    key     = "terraform/ecs-cluster/normal/task-def/service/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-2"
}

variable "template_version" {
  default = "1.1"
}

variable "cluster_name" {
  default = "normal"
}

# variables -----------------------------------------------
variable "awslog_region" {
  default = "ap-northeast-2"
}

variable "stages" {
  default = {
    default = {
        env_service_stage = "production"
        hosts = ["ecsdep.kracknet.com"]
        listener_priority = 10
        service_name = "service"
        task_definition_name = "service"
    }
    qa = {
        env_service_stage = "qa"
        hosts = ["ecsdep-qa.kracknet.com"]
        listener_priority = 11
        service_name = "service--qa"
        task_definition_name = "service--qa"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    cpu = 100
    desired = 1
    max = 4
    memory = 80
    min = 1
  }
}

variable "deployment_strategy" {
  default = {
    minimum_healthy_percent = 100
    maximum_percent = 200
  }
}

variable "exposed_container" {
  default = []
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
        matcher = "200,301,302,404"
    }
  }
}

variable "loggings" {
  default = ["skitai-app", "skitai-nginx"]
}

variable "loadbalancing_pathes" {
  default = ["/*"]
}

variable "requires_compatibilities" {
  default = ["EC2"]
}

variable "service_resources" {
  default = {
    memory = 386
    cpu = 256
  }
}

variable "vpc_name" {
  default = "main"
}

variable "force_new_deployment" {
  default = false
}