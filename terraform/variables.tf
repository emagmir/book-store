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