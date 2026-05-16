output "repository_url" {
  value = aws_ecr_repository.app_repository.repository_url
}

output "load_balancer_dns" {
  value = aws_lb.app_alb.dns_name
}
