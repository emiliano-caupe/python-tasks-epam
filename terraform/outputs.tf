output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.python_tasks.repository_url
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.python_tasks.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.python_tasks.arn
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = "${aws_apigatewayv2_stage.python_tasks.invoke_url}/run"
}
