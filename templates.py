# import json
# import logging
# import boto3



# def lambda_handler(event, context):
#     client = boto3.client('ssm')
#     result=client.get_parameter(Name="PLAIN_TEXT")['Parameter']['Value']
#     #return "Success"
#     print (result)
#     response = {'result': result}
#     return {
#         'statusCode': 200,
#         'body': response
        
#     }

# import json
# import logging
# import boto3

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# e = ""
# def lambda_handler(event, context):
#     try:
#         # Your existing authentication logic here...
#         username = event.get('username')

#         # If authentication is successful, log it as INFO
#         logger.info(f"Authentication successful for user: {username}")

#         # Your existing code to handle successful authentication...

#         return {
#             'statusCode': 200,
#             'body': 'Authentication successful'
#         }
#     except Exception as e:
#         # If authentication fails, log it as ERROR
#         logger.error(f"Authentication failed for user: {event.get('username', 'Unknown')}. Error: {str(e)}")


        # Your existing code to handle failed authentication...

        # return {
        #     'statusCode': 401,
        #     'body': 'Authentication failed'
        # }


def lambda_handler(event, context):
    # DynamoDB table name
    table_name = 'user-table-01'
    bucket_name = 'bucket-commit-01'
    
    
    
    # Extract user information from the event
    claims = event['requestContext']['authorizer']['claims']
    
    # Retrieve the name and email attributes from the claims
    name = claims.get('name')
    email = claims.get('email')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the file content
    file_content = f"Hello {name}, the current time is: {timestamp}"
    
    # Check if the attributes are present in the claims
    if name and email:
        # User attributes found success login, perform further processing
        
        client = boto3.client('ssm')
        result=client.get_parameter(Name="PLAIN_TEXT")['Parameter']['Value']
        #return "Success"
        print (response)
        response = {'result': result}
        return response

        # Write user information to DynamoDB
        dynamodb_resource = boto3.resource("dynamodb")
        table = dynamodb_resource.Table(table_name)
        #inserting values into table
        response = table.put_item(
        Item={
                "username": name,
                "timestamp": timestamp,
            }
        )


        # Upload the file to the S3 bucket
        s3_client = boto3.client('s3')
        bucket_name = bucket_name
        new_name = name.replace(" ", "_")
        file_name = f"{new_name}.txt"
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        
        
        # logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    
        # If authentication is successful, log it as INFO
        logger.info(f"Authentication successful for user: {name}")
    

        # return {
        #     'statusCode': 200,
        #     'body': json.dumps(response, indent=2) + 'Success db updated' + json.dumps({'name': name, 'email': email, 'timestamp': timestamp, 'file_name': file_name})
        # }

       


        return {
            'statusCode': 200,
            'body': json.dumps(response, indent=2) + 'Success db updated, file uploaded to s3 and ssm, values: ' + json.dumps({'name': name, 'email': email, 'timestamp': timestamp, 'file_name': file_name})
        }
    
    else:
        # User attributes not found, handle the error
        return {
            'statusCode': 400,
            'body': 'Name and email attributes not found in claims, unsuccesful login'
        }
