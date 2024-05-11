resource "aws_key_pair" "default" {
    count      = var.autoscale.min > 0 ? 1:0
    key_name   = var.cluster_name
    public_key = file (var.public_key_file)
}

resource "aws_iam_instance_profile" "profile" {
  count = length (aws_key_pair.default) > 0 ? 1:0
  name  = "${var.cluster_name}-profile"
  role  = aws_iam_role.ecs_host_role.name
}

data "aws_ami" "latest_ecs" {
  count       = var.ami != "" ? 1:0
  most_recent = true
  filter {
    name   = "name"
    values = [var.ami]
  }

 filter {
   name   = "owner-alias"
   values = ["amazon"]
 }
}

data "aws_security_group" "vpc-default" {
  filter {
    name   = "group-name"
    values = ["default"]
  }
  filter {
    name   = "vpc-id"
    values = [var.vpc.cidr_block == "" ? data.aws_vpc.default.id : aws_vpc.main[0].id]
  }
}

resource "aws_launch_template" "host" {
    count                       = length (aws_key_pair.default) > 0 ? 1:0
    name                        = var.cluster_name
    image_id                    = data.aws_ami.latest_ecs [0].id
    instance_type               = var.instance_type
    iam_instance_profile {
      name = aws_iam_instance_profile.profile [0].name
    }
    monitoring {
      enabled = true
    }
    network_interfaces {
      security_groups             = [ data.aws_security_group.vpc-default.id, aws_security_group.host [0].id ]
      associate_public_ip_address = true
    }
    key_name                    = aws_key_pair.default [0].key_name
    user_data                   = base64encode ("#!/bin/bash\necho ECS_CLUSTER='${var.cluster_name}' > /etc/ecs/ecs.config")
    tag_specifications {
      resource_type             = "instance"
      tags = {
        Name                    = var.cluster_name
        system                  = var.cluster_name
      }
    }
    tag_specifications {
      resource_type               = "volume"
      tags = {
        Name                    = var.cluster_name
      }
  }
}
