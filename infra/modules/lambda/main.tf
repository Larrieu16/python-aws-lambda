resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

module "hello_lambda" {
  source           = "../../lambda"
  function_name    = "hello-python"
  filename         = "${path.module}/../../../../lambda/helloWorld/hello.zip"
  handler = "helloHandler.lambda_handler"
  role_arn         = aws_iam_role.lambda_exec.arn
  environment_variables = {}
}
