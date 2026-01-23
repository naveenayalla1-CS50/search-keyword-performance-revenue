resource "aws_glue_job" "this" {
  name     = var.project_name
  role_arn = aws_iam_role.glue_role.arn

  glue_version = "4.0"
  number_of_workers = 2
  worker_type = "G.1X"
  timeout = 10

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = var.glue_script_s3_path
  }

  default_arguments = {
    "--INPUT_FILE" = var.input_file
    "--job-language" = "python"
    "--enable-continuous-cloudwatch-log" = "true"
  }
}
