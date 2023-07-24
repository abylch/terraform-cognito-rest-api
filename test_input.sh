#!/bin/bash

# Prompt for username and password
read -p "Enter your Cognito username: " username
read -s -p "Enter your Cognito password: " password
echo # Move to the next line after password input

user_pool_id=$(terraform output -raw user_pool_id)
api_gateway_arn=$(terraform output -raw  api_gateway_arn | cut -d ":" -f 6)
client_id=$(terraform output -raw client_id)

echo "api_gateway_arn: $api_gateway_arn"
echo "User pool id: $user_pool_id"
echo "Client id of the cognito user pool client: $client_id"

TOKEN=$(aws cognito-idp initiate-auth \
    --auth-flow USER_PASSWORD_AUTH \
    --client-id $client_id \
    --auth-parameters USERNAME=$username,PASSWORD=$password \
    --query 'AuthenticationResult.IdToken' \
    --output text)

echo TOKEN: $TOKEN

curl -X GET https://$api_gateway_arn.execute-api.us-west-1.amazonaws.com/stage-01/users \
    -H "Authorization: Bearer $TOKEN"

# Testing CORS
# curl -v -X OPTIONS https://{restapi_id}.execute-api.{region}.amazonaws.com/{stage_name}
# curl -v -X OPTIONS https://8cy8pdppng.execute-api.us-west-1.amazonaws.com/stage-01/users
# curl -v -X OPTIONS https://$api_gateway_arn.execute-api..us-west-1.amazonaws.com/stage-01/users

