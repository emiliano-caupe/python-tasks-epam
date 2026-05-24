terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ECR – stores the Docker image

resource "aws_ecr_repository" "python_tasks" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  lifecycle {
    ignore_changes = [tags]
  }
}

resource "aws_ecr_lifecycle_policy" "python_tasks" {
  repository = aws_ecr_repository.python_tasks.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep only last 5 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      }
      action = { type = "expire" }
    }]
  })
}

# IAM Role – Lambda execution

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${var.project_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function – container image

resource "aws_lambda_function" "python_tasks" {
  function_name = var.project_name
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.python_tasks.repository_url}:latest"

  timeout     = 30
  memory_size = 128

  environment {
    variables = {
      ENV = var.environment
    }
  }
}

# API Gateway – expone Lambda como HTTP

resource "aws_apigatewayv2_api" "python_tasks" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_integration" "python_tasks" {
  api_id                 = aws_apigatewayv2_api.python_tasks.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.python_tasks.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "python_tasks" {
  api_id    = aws_apigatewayv2_api.python_tasks.id
  route_key = "GET /run"
  target    = "integrations/${aws_apigatewayv2_integration.python_tasks.id}"
}

resource "aws_apigatewayv2_stage" "python_tasks" {
  api_id      = aws_apigatewayv2_api.python_tasks.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.python_tasks.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.python_tasks.execution_arn}/*/*"
}