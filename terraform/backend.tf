terraform {
  backend "s3" {
    bucket         = "restaurant-api-tfstate"
    key            = "restaurant-api/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
