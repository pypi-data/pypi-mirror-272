terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "h3lab-states-data"
    key     = "terraform/ecs-cluster/novpc/task-def/novpc-service/terraform.tfstate"
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
  default = "novpc"
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
        service_name = "novpc-service"
        task_definition_name = "novpc-service"
    }
    qa = {
        env_service_stage = "qa"
        hosts = ["ecsdep-qa.kracknet.com"]
        listener_priority = 11
        service_name = "novpc-service--qa"
        task_definition_name = "novpc-service--qa"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    desired = 1
    min = 1
    max = 4
    cpu = 100
    memory = 80
  }
}

variable "deployment_strategy" {
  default = {
    minimum_healthy_percent = 100
    maximum_percent = 200
  }
}

variable "exposed_container" {
  default = [{
    name = "skitai-nginx"
    port = 80
  }]
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/ping"
        matcher = "200,301,302,404"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
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
  default = ""
}

variable "force_new_deployment" {
  default = false
}