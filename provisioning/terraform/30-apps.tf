#
# This file is used to define compute resources for applications

# Application
#
# This resource relies on the Heroku Terraform provider being previously configured.
#
# AWS source: https://devcenter.heroku.com/articles/how-heroku-works#defining-an-application
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/app.html
resource "heroku_app" "bas-style-kit-file-upload" {
  name   = "bas-style-kit-file-upload"
  region = "eu"
}
