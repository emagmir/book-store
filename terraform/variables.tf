variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "clusterName" {
  description = "Name of EKS cluster"
  type        = string
  default     = "book-store-eks"
}

variable "personal_ip" {
  description = "Personal IP address for SSH access"
  type        = string
}

variable "account_id" {
  description = "AWS account id"
  type = string
}