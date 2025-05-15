module "hello_lambda" {
  source           = "../../lambda"
  function_name    = "hello-python"
  filename         = "${path.module}/../../../../lambda/helloWorld/hello.zip"
  handler = "helloHandler.lambda_handler"
  role_arn         = aws_iam_role.lambda_exec.arn
  environment_variables = {}
}
