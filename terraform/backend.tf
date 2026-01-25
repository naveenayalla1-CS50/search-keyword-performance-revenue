terraform {
  backend "s3" {
    bucket         = "naveen-terraform-state-821891894533"
    key            = "search-keyword-performance/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
