#!/bin/bash

# Fetch the personal IP address using curl
PERSONAL_IP=$(curl -s ifconfig.me)

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Export the IP address as a Terraform variable
export TF_VAR_personal_ip="${PERSONAL_IP}/32"
export TF_VAR_account_id="${ACCOUNT_ID}"
