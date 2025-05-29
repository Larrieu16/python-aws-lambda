variable "lambda_hello_invoke_arn" {
  description = "ARN de invocação da função Lambda hello"
  type        = string
}

variable "lambda_get_items_invoke_arn" {
  description = "ARN de invocação da função Lambda get_items"
  type        = string
}

variable "lambda_create_item_invoke_arn" {
  description = "ARN de invocação da função Lambda create_item"
  type        = string
}

variable "lambda_hello_function_name" {
  type = string
}

variable "lambda_get_items_function_name" {
  type = string
}

variable "lambda_create_item_function_name" {
  type = string
}

variable "cognito_user_pool_id" {
  type        = string
  description = "ID do Cognito User Pool"
}

variable "cognito_client_id" {
  type        = string
  description = "ID do App Client do Cognito User Pool"
}