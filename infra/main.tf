
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
  source                = "./modules/lambda"
  function_name         = "create-item"
  filename              = data.archive_file.add_item_zip.output_path
  handler               = "add_handler.lambda_handler"
  role_arn              = aws_iam_role.lambda_exec.arn
  environment_variables = {
     DYNAMODB_TABLE = module.dynamodb.table_name

  }
}

module "delete_item_lambda" {
  source                = "./modules/lambda"
  function_name         = "delete-item"
  filename              = data.archive_file.delete_item_zip.output_path
  handler               = "delete_handler.lambda_handler"
  role_arn              = aws_iam_role.lambda_exec.arn
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name
  }
}

module "update_item_lambda" {
  source                = "./modules/lambda"
  function_name         = "update-item"
  filename              = data.archive_file.update_item_zip.output_path
  handler               = "update_handler.lambda_handler"
  role_arn              = aws_iam_role.lambda_exec.arn
  environment_variables = {
     DYNAMODB_TABLE = module.dynamodb.table_name

  }
  
}

module "dynamodb" {
  source = "./modules/dynamodb"  # caminho relativo para a pasta do módulo
}
