# variable.tf

## AWS account level config: region
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}

## AWS S3 bucket details
variable "bucket_prefix" {
  description = "Bucket prefix for our datalake"
  type        = string
  default     = "de-data-lake-"
}