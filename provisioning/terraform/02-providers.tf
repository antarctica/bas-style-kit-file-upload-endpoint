#
# This file is used to define Terraform provider resources

# Heroku provider
#
# Provider for experiments and prototypes
#
# See https://www.terraform.io/docs/providers/aws/index.html#authentication for how to
# configure credentials to use this provider.
#
# AWS source: https://heroku.com
# Terraform source: https://www.terraform.io/docs/providers/heroku/index.html
provider "heroku" {
  version = "~> 1.3"
}
