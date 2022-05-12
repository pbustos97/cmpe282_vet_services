import json
import logging
import boto3
import os
from Clinic import Clinic
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
        return returnResponse(400, {'message': 'Invalid input, no body'})
    
    if 'clinicId' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no clinic'})
    
    if eventBody['clinicId'] == '-1':
        clinics = getClinicAll()
        if clinics == None:
            return returnResponse(500, {'message': 'No clinics found',
                                       'status': 'error'})
        return returnResponse(200, {'message': '{} clinics found'.format(len(clinics)),
                                    'status': 'success',
                                    'clinics': clinics})
        
    clinic = getClinic(eventBody['clinicId'])
    if (clinic == None):
        return returnResponse(400, {'message': 'Invalid input, clinic does not exist',
                                    'status': 'error'})

    return returnResponse(200, {'message': 'clinic found',
                                'status': 'success',
                                'clinic': clinic.toJson()})
    
def getClinic(clinicId):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    clinicTable = dynamodb.Table(os.environ['TABLE_CLINIC'])
    try:
        item = clinicTable.get_item(
            TableName=os.environ['TABLE_CLINIC'],
            Key={
                'clinicId': clinicId
            }
        )
        if 'Item' not in item:
            return None
        return Clinic(clinicId, item['Item']['clinicName'], item['Item']['email'] , item['Item']['Address'], item['Item']['Country'], item['Item']['ownerId'])
    except ClientError as e:
        return returnResponse(400, e.response['Error']['Message'])

# Should return all clinics inside of DynamoDB table
def getClinicAll():
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    clinicTable = dynamodb.Table(os.environ['TABLE_CLINIC'])
    try:
        item = clinicTable.scan(
            ProjectionExpression = "clinicId, clinicName, email, ownerId, Address"
        )
        logger.debug('[DEBUG] item: {}'.format(item))
        if 'Items' not in item:
            return None
        return item['Items']
    except ClientError as e:
        return returnResponse(400, e.response['Error']['Message'])

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