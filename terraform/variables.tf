variable "region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "search-keyword-performance"
}

variable "glue_script_s3_path" {
  description = "S3 path to glue_job.py"
}

variable "input_file" {
  description = "S3 path of input CSV file"
}

variable "output_bucket" {
  description = "S3 bucket for output"
}
