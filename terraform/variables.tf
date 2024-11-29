variable "access_key_id" {
  description = "access key for aws"
  type        = string
}

variable "secret_access_key" {
  description = "secret access key for AWS"
  type        = string
}

variable "db_host" {
  description = "host address for the database"
  type        = string
}

variable "db_port" {
  description = "port for the database connection"
  type        = string
}

variable "db_password" {
  description = "password for the database user"
  type        = string
}

variable "db_user" {
  description = "database user name"
  type        = string
}

variable "db_name" {
  description = "name of the database"
  type        = string
}

variable "schema_name" {
  description = "schema name in the database"
  type        = string
}