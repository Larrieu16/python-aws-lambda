variable "function_name" {}
variable "filename" {}
variable "handler" {}
variable "role_arn" {}
variable "environment_variables" {
  type    = map(string)
  default = {}
}
variable "timeout" {
  type    = number
  default = 30
}
