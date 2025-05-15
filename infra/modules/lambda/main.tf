resource "aws_lambda_function" "this" {
  function_name = var.function_name
  filename      = var.filename
  handler       = var.handler
  runtime       = "python3.11"
  role          = var.role_arn
  source_code_hash = filebase64sha256(var.filename)

  environment {
    variables = var.environment_variables
  }
}
