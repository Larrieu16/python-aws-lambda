resource "aws_dynamodb_table" "tabela_mercado" {
  name         = "TabelaMercado"
  billing_mode = "PAY_PER_REQUEST" # Sem necessidade de provisionar RCU/WCU
  hash_key     = "PK"              # Partition key
  range_key    = "SK"              # Sort key

  attribute {
    name = "PK"
    type = "S" # S = String
  }

  attribute {
    name = "SK"
    type = "S"
  }

  tags = {
    Environment = "dev"
    Project     = "mercado"
  }
}

output "table_name" {
  value = aws_dynamodb_table.tabela_mercado.name
}

output "table_arn" {
  value = aws_dynamodb_table.tabela_mercado.arn
}
