variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-2"
}

variable "project_name" {
  type        = string
  description = "Project prefix for names"
  default     = "search-keyword-performance"
}

variable "glue_version" {
  type        = string
  description = "Glue version (e.g., 4.0 or 5.0)"
  default     = "5.0"
}

variable "glue_worker_type" {
  type        = string
  description = "Glue worker type"
  default     = "G.1X"
}

variable "glue_number_of_workers" {
  type        = number
  description = "Number of Glue workers"
  default     = 2
}

# Your existing buckets (do NOT create if already exist)
variable "raw_bucket" {
  type        = string
  description = "Raw input bucket name"
  default     = "ad-raw-artifacts"
}

variable "processed_bucket" {
  type        = string
  description = "Output bucket name"
  default     = "ad-processed-artifacts"
}

variable "artifacts_bucket" {
  type        = string
  description = "Artifacts bucket name (script, zips)"
  default     = "ad-glue-artifacts"
}

# Paths inside artifacts bucket
variable "glue_script_key" {
  type        = string
  description = "S3 key for Glue script"
  default     = "jobs/search_keyword_performance_glue.py"
}

variable "extra_py_files_key" {
  type        = string
  description = "S3 key for extra py files zip"
  default     = "jobs/glue-helper.zip"
}

# Glue default args
variable "temp_dir_bucket" {
  type        = string
  description = "Glue TempDir bucket (AWS managed assets bucket is fine)"
  default     = "" # set in tfvars if you want: aws-glue-assets-xxxx-region
}

variable "input_file" {
  type        = string
  description = "Default input file S3 URI"
  default     = "s3://ad-raw-artifacts/input/dt=23-01-2026/data.tsv"
}

variable "output_base_path" {
  type        = string
  description = "Default output base path S3 URI"
  default     = "s3://ad-processed-artifacts/results/"
}
