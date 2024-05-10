resource "aws_security_group" "load_balancer" {
    count       = var.cert_name != "" ? 1:0
    name        = "${var.cluster_name}-load-balancer"
    description = "allows http(s)"
    vpc_id      = var.vpc.cidr_block == "" ? data.aws_vpc.default.id : aws_vpc.main[0].id

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "${var.cluster_name}-load-balancer"
    }
}

resource "aws_alb" "load_balancer" {
    count           = length (aws_security_group.load_balancer) > 0 ? 1:0
    name            = var.cluster_name
    security_groups = [ aws_security_group.load_balancer [0].id ]
    subnets         = var.vpc.cidr_block == "" ? toset(data.aws_subnets.default.ids) : [ for each in aws_subnet.public: each.id ]
    enable_http2    = true
    idle_timeout    = 600
    tags = {
        Name = var.cluster_name
    }
}

resource "aws_alb_listener" "front_end_80" {
  count    = length (aws_alb.load_balancer) > 0 ? 1:0
  load_balancer_arn = aws_alb.load_balancer [0].id
  port     = 80
  protocol = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_alb_target_group" "default" {
  count    = length (aws_alb.load_balancer) > 0 ? 1:0
  name     = "${var.cluster_name}-empty"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc.cidr_block == "" ? data.aws_vpc.default.id : aws_vpc.main[0].id
}

resource "aws_alb_listener" "front_end" {
  count             = length (aws_alb.load_balancer) > 0 ? 1:0
  load_balancer_arn = aws_alb.load_balancer [0].id
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = data.aws_acm_certificate.cert [0].arn

  default_action {
    target_group_arn = aws_alb_target_group.default [0].id
    type             = "forward"
  }
  tags = {
    Name = var.cluster_name
  }
}
