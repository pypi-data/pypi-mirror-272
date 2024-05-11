terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "h3lab-states-data"
    key     = "terraform/ecs-cluster/noec2/terraform.tfstate"
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
  default = "noec2"
}

variable "instance_type" {
  default = ""
}

variable "ami" {
  default = ""
}

variable "cors_hosts" {
  default = []
}

variable "cert_name" {
  default = ""
}

variable "public_key_file" {
  default = ""
}

variable "autoscale" {
  default = {
    desired = 0
    min = 0
    max = 1
    cpu = 0
    memory = 0
    target_capacity = 0
  }
}

variable "az_count" {
  default = 3
}

variable "task_iam_policies" {
  default = []
}

variable "vpc" {
  default = {
    cidr_block = ""
    octet3s = [10, 20, 30]
    peering_vpc_ids = []
  }
}