locals {
  artifacts_bucket_uri = "s3://${var.artifacts_bucket}"
  script_location      = "${local.artifacts_bucket_uri}/${var.glue_script_key}"
  extra_py_files       = "${local.artifacts_bucket_uri}/${var.extra_py_files_key}"
  temp_dir             = var.temp_dir_bucket == "" ? null : "s3://${var.temp_dir_bucket}/temporary/"
}

resource "aws_glue_job" "job" {
  name     = var.project_name
  role_arn = aws_iam_role.glue_role.arn

  glue_version = var.glue_version

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = local.script_location
  }

  worker_type       = var.glue_worker_type
  number_of_workers = var.glue_number_of_workers
  timeout           = 60

  default_arguments = merge(
    {
      "--JOB_NAME"               = var.project_name
      "--INPUT_FILE"             = var.input_file
      "--OUTPUT_BASE_PATH"       = var.output_base_path
      "--enable-metrics"         = "true"
      "--enable-spark-ui"        = "true"
      "--enable-job-insights"    = "true"
      "--enable-observability-metrics" = "true"
      "--job-bookmark-option"    = "job-bookmark-disable"
      "--extra-py-files"         = local.extra_py_files
    },
    local.temp_dir == null ? {} : { "--TempDir" = local.temp_dir }
  )
}
