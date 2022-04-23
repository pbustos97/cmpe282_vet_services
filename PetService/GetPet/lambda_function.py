import json
import logging
import boto3
import os
from Pet import Pet
from botocore.exceptions import ClientError

# from dotenv import load_dotenv
# load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    # Required since we want a unified input event
    eventBody = event
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)

    if 'queryStringParameters' in eventBody:
        eventBody = eventBody['queryStringParameters']
    else:
        return returnResponse(400, {'message': 'Invalid input, no body',
                                     'status': 'error'})
    
    if 'userId' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no user',
                                     'status': 'error'})
    if 'petId' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no pet',
                                     'status': 'error'})

    # Remove keys and regions when done
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    userTable = dynamodb.Table(os.environ['TABLE_USER'])
    try:
        item = userTable.get_item(
            TableName=os.environ['TABLE_USER'],
            Key={
                'userId': eventBody['userId'],
                'petId': eventBody['petId']
            }
        )
        if 'Item' not in item:
            return returnResponse(400, {'message': 'Invalid userId, user does not exist', 'status': 'error'})
        p = Pet(item['Item']['name'], item['Item']['age'], item['Item']['ownerId'], item['Item']['petId'], item['Item']['breed'], item['Item']['species'], item['Item']['weight'])
    except ClientError as e:
        return returnResponse(400, e.response['Error']['Message'])
    return returnResponse(200, {'pet': p.toJson(), 'status': 'success'})

def returnResponse(statusCode, body):
    logger.debug('[RESPONSE] statusCode: {} body: {}'.format(statusCode, body))
    logger.debug('[RESPONSE] json.dumps(body): {}'.format(json.dumps(body)))
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'isBase64Encoded': False,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            'Access-Control-Allow-Credentials': True,
            'Content-Type': 'application/json'
        }
    }