#!/bin/bash

user_pool_id=$(terraform output -raw user_pool_id)
#api_gateway_arn=$(terraform output -raw  api_gateway_arn | cut -d ":" -f 6)
client_id=$(terraform output -raw client_id)

#echo "api_gateway_arn: $api_gateway_arn"
echo "User pool id: $user_pool_id"
echo "Client id of the cognito user pool client: $client_id"

# Prompt for username, password, and name
read -p "Enter your Cognito username: " username
echo # Move to the next line after username input
echo "Please enter your password 8 characters, 1 number, and 1 special character, and 1 capital letter"
read -s -p "Enter your Cognito password: " password
echo # Move to the next line after password input
read -p "Enter your name: " name

aws cognito-idp sign-up \
    --client-id $client_id \
    --username "$username" \
    --password "$password" \
    --user-attributes Name="email",Value="$username" Name="name",Value="$name" \
    --region us-west-1 \
    --profile default

aws cognito-idp admin-confirm-sign-up \
    --user-pool-id $user_pool_id \
    --username "$username" \
    --region us-west-1 \
    --profile default

aws cognito-idp admin-update-user-attributes \
    --user-pool-id $user_pool_id \
    --username "$username" \
    --user-attributes Name=email_verified,Value=true \
    --region us-west-1 \
    --profile default
