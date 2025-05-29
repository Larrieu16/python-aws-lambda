# Resources
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

resource "aws_iam_role_policy" "lambda_inline_policy" {
  name = "LambdaDynamoDBRWPolicy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:GetItem",
          "dynamodb:query",
          "dynamodb:Scan"
        ],
        Resource = module.dynamodb.table_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create a zip file for each Lambda function

data "archive_file" "add_item_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/api/add_item"
  output_path = "${path.module}/build/add.zip"
}

data "archive_file" "delete_item_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/api/delete_item"
  output_path = "${path.module}/build/delete.zip"
}

data "archive_file" "hello_world_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/api/hello_world"
  output_path = "${path.module}/build/hello.zip"
}

data "archive_file" "update_item_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/api/update_item"
  output_path = "${path.module}/build/update.zip"
}

data "archive_file" "get_items_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/api/get_items"
  output_path = "${path.module}/build/get-items.zip"
}

# Lambda Modules
module "hello_lambda" {
  source                = "./modules/lambda"
  function_name         = "hello-python"
  filename              = data.archive_file.hello_world_zip.output_path
  handler               = "hello_handler.lambda_handler"
  role_arn              = aws_iam_role.lambda_exec.arn
  environment_variables = {}
}

module "create_item_lambda" {
  source        = "./modules/lambda"
  function_name = "create-item"
  filename      = data.archive_file.add_item_zip.output_path
  handler       = "add_handler.lambda_handler"
  role_arn      = aws_iam_role.lambda_exec.arn
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name

  }
}

module "delete_item_lambda" {
  source        = "./modules/lambda"
  function_name = "delete-item"
  filename      = data.archive_file.delete_item_zip.output_path
  handler       = "delete_handler.lambda_handler"
  role_arn      = aws_iam_role.lambda_exec.arn
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name
  }
}

module "update_item_lambda" {
  source        = "./modules/lambda"
  function_name = "update-item"
  filename      = data.archive_file.update_item_zip.output_path
  handler       = "update_handler.lambda_handler"
  role_arn      = aws_iam_role.lambda_exec.arn
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name

  }

}

module "get_items_lambda" {
  source        = "./modules/lambda"
  function_name = "get-items"
  filename      = data.archive_file.get_items_zip.output_path
  handler       = "get_items_handler.lambda_handler"
  role_arn      = aws_iam_role.lambda_exec.arn
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name
  }
}

module "dynamodb" {
  source = "./modules/dynamodb" # caminho relativo para a pasta do módulo
}

module "cognito" {
  source = "./modules/cognito"
}

module "api_gateway" {
  source                         = "./modules/api-gateway"
  lambda_hello_invoke_arn        = module.hello_lambda.lambda_invoke_arn
  lambda_get_items_invoke_arn    = module.get_items_lambda.lambda_invoke_arn
  lambda_add_item_invoke_arn     = module.create_item_lambda.lambda_invoke_arn
  lambda_hello_function_name     = module.hello_lambda.function_name
  lambda_get_items_function_name = module.get_items_lambda.function_name
  lambda_add_item_function_name  = module.create_item_lambda.function_name
  cognito_user_pool_id           = module.cognito.user_pool_id
  cognito_client_id              = module.cognito.client_id
}

output "api_gateway_url" {
  value = module.api_gateway.api_endpoint
}

output "cognito_user_pool_id" {
  value = module.cognito.user_pool_id
}

output "cognito_client_id" {
  value = module.cognito.client_id
}

