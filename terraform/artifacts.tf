# These files must exist on the machine running terraform (GitHub Actions runner)
variable "local_glue_script_path" {
  type        = string
  description = "Local path to glue script"
  default     = "../glue_job.py"
}

variable "local_extra_py_zip_path" {
  type        = string
  description = "Local path to glue helper zip"
  default     = "../dist/glue-helper.zip"
}

resource "aws_s3_object" "glue_script" {
  bucket = var.artifacts_bucket
  key    = var.glue_script_key
  source = var.local_glue_script_path
  etag   = filemd5(var.local_glue_script_path)
}

resource "aws_s3_object" "extra_py_zip" {
  bucket = var.artifacts_bucket
  key    = var.extra_py_files_key
  source = var.local_extra_py_zip_path
  etag   = filemd5(var.local_extra_py_zip_path)
}
