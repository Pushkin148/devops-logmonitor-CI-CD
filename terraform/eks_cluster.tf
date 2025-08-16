
# EKS Cluster (control plane)

resource "aws_eks_cluster" "this" {
  name     = "${var.cluster_name}"
  version  = var.eks_version
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids              = [aws_subnet.private_1.id, aws_subnet.private_2.id] # control plane endpoints in private subnets
    endpoint_public_access  = true   # allow kubectl via public endpoint (can be tightened later)
    endpoint_private_access = true   # also enable private endpoint inside VPC
  }

  tags = {
    Name = "${var.cluster_name}"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.eks_cluster_AmazonEKSVPCResourceController
  ]
}


# EKS Managed Node Group

resource "aws_eks_node_group" "default" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-ng"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = [aws_subnet.private_1.id, aws_subnet.private_2.id] # nodes in private subnets (recommended)

  scaling_config {
    desired_size = var.node_desired_capacity
    min_size     = var.node_min_size
    max_size     = var.node_max_size
  }

  capacity_type = "ON_DEMAND"
  instance_types = var.node_instance_types

  ami_type = "AL2_x86_64" # default Amazon Linux 2 for x86; change if you need ARM

  tags = {
    Name = "${var.cluster_name}-ng"
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly
  ]
}
