################################################################################
## workspace variables

variable "availability_zone" {
  default = "ap-southeast-2c"
}

variable "umccrise_image_id" {
  default = "ami-03037fc9d9ca37131"
}

variable "stack_name" {
  default = "agha_batch"
}

variable "slack_lambda_arn" {
  default = "arn:aws:lambda:ap-southeast-2:620123204273:function:bootstrap_slack_lambda_dev"
}

variable "fleet_instance_types" {
  type = "list"
  default = ["m4.large", "t3.medium"]
}


variable "workspace_umccrise_data_bucket" {
  type = "map"

  default = {
    prod = "umccr-primary-data-prod"
    dev  = "umccr-primary-data-dev"
  }
}

variable "workspace_umccrise_refdata_bucket" {
  type = "map"

  default = {
    prod = "umccr-umccrise-refdata-prod"
    dev  = "umccr-umccrise-refdata-dev"
  }
}

variable "workspace_umccrise_buckets" {
  type = "map"

  default = {
    prod = ["arn:aws:s3:::umccr-primary-data-prod", "arn:aws:s3:::umccr-primary-data-prod/*", "arn:aws:s3:::umccr-umccrise-prod", "arn:aws:s3:::umccr-umccrise-prod/*", "arn:aws:s3:::umccr-umccrise-refdata-prod", "arn:aws:s3:::umccr-umccrise-refdata-prod/*"]
    dev  = ["arn:aws:s3:::umccr-primary-data-dev", "arn:aws:s3:::umccr-primary-data-dev/*", "arn:aws:s3:::umccr-umccrise-dev", "arn:aws:s3:::umccr-umccrise-dev/*", "arn:aws:s3:::umccr-umccrise-refdata-dev", "arn:aws:s3:::umccr-umccrise-refdata-dev/*"]
  }
}