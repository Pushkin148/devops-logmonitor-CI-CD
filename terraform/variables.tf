# AWS Region
variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

# VPC
variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

# Subnets
variable "public_subnet_cidr_1" {
  description = "CIDR block for Public Subnet 1"
  type        = string
}

variable "public_subnet_cidr_2" {
  description = "CIDR block for Public Subnet 2"
  type        = string
}

variable "private_subnet_cidr_1" {
  description = "CIDR block for Private Subnet 1"
  type        = string
}

variable "private_subnet_cidr_2" {
  description = "CIDR block for Private Subnet 2"
  type        = string
}

# Cluster Name (optional, for future EKS)
variable "cluster_name" {
  description = "Name prefix for resources"
  type        = string
}

# EKS version (e.g., "1.29" or "1.30" — pick what's available in your region)
variable "eks_version" {
  description = "EKS Kubernetes version"
  type        = string
  default     = "1.29"
}

# Node group size
variable "node_desired_capacity" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

# EC2 instance types for worker nodes
variable "node_instance_types" {
  description = "List of instance types for the EKS node group"
  type        = list(string)
  default     = ["t3.medium"]
}
