
variable "region" {
  default = "us-east-1"
}

variable "availability_zone" {
  default = "us-east-1a"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-12345678" # Replace with a valid Amazon Linux or Ubuntu AMI ID
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  default     = "s3-list-bucket-example"
}
