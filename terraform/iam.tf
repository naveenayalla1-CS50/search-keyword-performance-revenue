data "aws_caller_identity" "current" {}

# Trust policy: allow AWS Glue service to assume this role
data "aws_iam_policy_document" "glue_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

# Glue execution role
resource "aws_iam_role" "glue_role" {
  name               = "${var.project_name}-glue-role"
  assume_role_policy = data.aws_iam_policy_document.glue_assume.json
}

# Permissions for Glue job to read input, read artifacts, write output, and write logs
data "aws_iam_policy_document" "glue_policy" {

  statement {
    sid     = "CloudWatchLogs"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams"
    ]
    resources = ["*"]
  }

  # Read input from raw bucket
  statement {
    sid     = "ReadRaw"
    actions = ["s3:ListBucket", "s3:GetObject"]
    resources = [
      "arn:aws:s3:::${var.raw_bucket}",
      "arn:aws:s3:::${var.raw_bucket}/*"
    ]
  }

  # Write output to processed bucket
  statement {
    sid     = "WriteProcessed"
    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation",
      "s3:PutObject",
      "s3:AbortMultipartUpload"
    ]
    resources = [
      "arn:aws:s3:::${var.processed_bucket}",
      "arn:aws:s3:::${var.processed_bucket}/*"
    ]
  }

  # Read artifacts (script + zip) from artifacts bucket
  statement {
    sid     = "ReadArtifacts"
    actions = ["s3:ListBucket", "s3:GetObject"]
    resources = [
      "arn:aws:s3:::${var.artifacts_bucket}",
      "arn:aws:s3:::${var.artifacts_bucket}/*"
    ]
  }

  # TempDir access (optional) if you provide temp_dir_bucket
  dynamic "statement" {
    for_each = var.temp_dir_bucket == "" ? [] : [1]
    content {
      sid     = "TempDirAccess"
      actions = ["s3:ListBucket", "s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
      resources = [
        "arn:aws:s3:::${var.temp_dir_bucket}",
        "arn:aws:s3:::${var.temp_dir_bucket}/*"
      ]
    }
  }
}

# Create the custom IAM policy from the document
resource "aws_iam_policy" "glue_policy" {
  name   = "${var.project_name}-glue-policy"
  policy = data.aws_iam_policy_document.glue_policy.json
}

# Attach the custom policy to the Glue execution role
resource "aws_iam_role_policy_attachment" "attach_custom" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_policy.arn
}

# Attach AWS managed Glue service policy (helps with Glue internals/logging)
resource "aws_iam_role_policy_attachment" "attach_managed" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
