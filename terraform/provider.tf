provider "aws" {
  region = "eu-west-2"
}

terraform {
	required_providers {
		aws = {
	    version = "~> 5.77.0"
		}
  }
}
