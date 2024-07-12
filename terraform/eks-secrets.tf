data "aws_iam_policy_document" "book_store_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [module.eks.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:default:book-store-sa"]
    }
  }
}

resource "aws_iam_role" "eks_secrets_role" {
  assume_role_policy = data.aws_iam_policy_document.book_store_assume_role_policy.json
  name               = "eks_secrets_role"
}


resource "aws_iam_policy" "secrets_manager_policy" {
  name = "secrets-manager-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Resource = "arn:*:secretsmanager:*:*:secret:mongo_string-??????"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.eks_secrets_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}