data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "glue_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue_role" {
  name               = "${var.project_name}-glue-role"
  assume_role_policy = data.aws_iam_policy_document.glue_assume.json
}

# Minimum S3 + logs perms (tighter than AmazonS3FullAccess)
data "aws_iam_policy_document" "glue_policy" {
  statement {
    sid     = "CloudWatchLogs"
    actions = [
      "logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents",
      "logs:DescribeLogGroups","logs:DescribeLogStreams"
    ]
    resources = ["*"]
  }

  # Read input from raw bucket
  statement {
    sid     = "ReadRaw"
    actions = ["s3:GetObject","s3:ListBucket"]
    resources = [
      "arn:aws:s3:::${var.raw_bucket}",
      "arn:aws:s3:::${var.raw_bucket}/*"
    ]
  }

  # Write output to processed bucket
  statement {
    sid     = "WriteProcessed"
    actions = ["s3:PutObject","s3:AbortMultipartUpload","s3:ListBucket","s3:GetBucketLocation"]
    resources = [
      "arn:aws:s3:::${var.processed_bucket}",
      "arn:aws:s3:::${var.processed_bucket}/*"
    ]
  }

  # Read artifacts (script + zip)
  statement {
    sid     = "ReadArtifacts"
    actions = ["s3:GetObject","s3:ListBucket"]
    resources = [
      "arn:aws:s3:::${var.artifacts_bucket}",
      "arn:aws:s3:::${var.artifacts_bucket}/*"
    ]
  }

  # TempDir if provided
  dynamic "statement" {
    for_each = var.temp_dir_bucket == "" ? [] : [1]
    content {
      sid     = "TempDirAccess"
      actions = ["s3:PutObject","s3:GetObject","s3:ListBucket","s3:DeleteObject"]
      resources = [
        "arn:aws:s3:::${var.temp_dir_bucket}",
        "arn:aws:s3:::${var.temp_dir_bucket}/*"
      ]
    }
  }
}

resource "aws_iam_policy" "glue_policy" {
  name   = "${var.project_name}-glue-policy"
  policy = data.aws_iam_policy_document.glue_policy.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_policy.arn
}

# Glue service role managed policy is still useful
resource "aws_iam_role_policy_attachment" "attach_managed" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
