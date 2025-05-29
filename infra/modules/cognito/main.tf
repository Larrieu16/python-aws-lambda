resource "aws_cognito_user_pool" "user_pool" {
  name = "user_pool"

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 6
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

}

resource "aws_cognito_user_pool_client" "cognito_client" {
  name = "cognito-client"

  user_pool_id           = aws_cognito_user_pool.user_pool.id
  generate_secret        = false
  refresh_token_validity = 90

  allowed_oauth_flows_user_pool_client = true
  prevent_user_existence_errors        = "ENABLED"
  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

  allowed_oauth_flows  = ["code", "implicit"]
  allowed_oauth_scopes = ["email", "openid", "profile"]

  callback_urls = ["http://localhost:8080/callback"]

}

resource "aws_cognito_user_pool_domain" "cognito_domain" {
  domain       = "lnsi-domain-${random_id.suffix.hex}"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}

resource "random_id" "suffix" {
  byte_length = 4
}
