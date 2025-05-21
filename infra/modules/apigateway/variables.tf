variable "lambda_invoke_arn" {
  description = "ARN de invocação da função Lambda"
  type        = string
}

variable "lambda_function_name" {
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