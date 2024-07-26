#!/bin/bash
# Install service accounts
kubectl apply -f ../templates/secrets-serviceaccount.yaml
kubectl apply -f ../templates/lb-controller-serviceaccount.yaml

# Install aws-load-balancer-controller
# follow the guide from this: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=book-store-eks --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller

# Install csi-secrets-store
#follow the guide from this: https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_csi_driver.html
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install -n kube-system csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver
kubectl apply -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml