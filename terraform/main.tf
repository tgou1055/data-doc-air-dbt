## main.tf

## ---------------------- Specify cloud service (AWS) provider ----------------------
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.aws_region
  profile = "default"
}

## ---------------------- Create S3 Bucket (Datalake) ----------------------

# create s3 bucket resource
resource "aws_s3_bucket" "de-data-lake" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

# specify acl for bucket
resource "aws_s3_bucket_acl" "de-data-lake-acl" {
  bucket     = aws_s3_bucket.de-data-lake.id
  acl        = "public-read-write"
  depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}


# create s3 object owernship
resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
  bucket = aws_s3_bucket.de-data-lake.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.setting]
}

# set s3 public access scheme
resource "aws_s3_bucket_public_access_block" "setting" {
  bucket                  = aws_s3_bucket.de-data-lake.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}