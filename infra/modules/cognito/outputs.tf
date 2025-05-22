output "user_pool_id" {
  description = "ID do Cognito User Pool"
  value       = aws_cognito_user_pool.user_pool.id
}

output "client_id" {
  description = "ID do App Client do Cognito User Pool"
  value       = aws_cognito_user_pool_client.cognito_client.id
}