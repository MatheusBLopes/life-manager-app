provider "aws" {
  profile = terraform.workspace == "prod" ? "prodProfile" : "devProfile"
  region  = "us-east-1"
}
