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
