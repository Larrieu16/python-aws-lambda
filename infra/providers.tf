provider "aws" {
  region = "sa-east-1"
}

terraform {
  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
  }
}
