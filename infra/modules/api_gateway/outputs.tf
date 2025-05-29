output "base_url" {
  description = "URL base para o API Gateway"
  value       = "${aws_apigatewayv2_stage.lambda.invoke_url}/hello"
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.lambda.api_endpoint
}
