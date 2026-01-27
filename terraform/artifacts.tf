variable "local_glue_script_path" {
  type        = string
  description = "Local path to glue script"
  default     = null
}

variable "local_extra_py_zip_path" {
  type        = string
  description = "Local path to glue helper zip"
  default     = null
}

locals {
  glue_script_path  = coalesce(var.local_glue_script_path, "${path.module}/../glue_job.py")
  extra_py_zip_path = coalesce(var.local_extra_py_zip_path, "${path.module}/../dist/glue-helper.zip")
}

resource "aws_s3_object" "glue_script" {
  bucket = var.artifacts_bucket
  key    = var.glue_script_key
  source = local.glue_script_path
  etag   = filemd5(local.glue_script_path)
}

resource "aws_s3_object" "extra_py_zip" {
  bucket = var.artifacts_bucket
  key    = var.extra_py_files_key
  source = local.extra_py_zip_path
  etag   = filemd5(local.extra_py_zip_path)
}
