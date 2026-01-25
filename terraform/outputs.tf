output "glue_job_name" {
  value = aws_glue_job.job.name
}

output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}

output "glue_script_s3" {
  value = "s3://${var.artifacts_bucket}/${var.glue_script_key}"
}
