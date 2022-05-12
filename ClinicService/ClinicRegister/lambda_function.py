import json
import logging
import boto3
import os
from Clinic import Clinic
from Doctor import Doctor
from User import User
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

    if 'body' in eventBody:
        eventBody = eventBody['body']
    else:
        return returnResponse(400, {'message': 'Invalid input, no body'})
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)
    
    if 'clinic' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no clinic object'})
    eventBody = eventBody['clinic']
    if 'clinicId' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no clinic'})
    if 'address' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no address'})
    if 'country' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no country'})
    if 'email' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no email'})
    if 'name' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no name'})
    if 'userId' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no userId. Cannot validate if doctor'})
    u = getUser(eventBody['userId'])
    if u is None:
        return returnResponse(400, {'message': 'Invalid userId',
                                    'status': 'error'})
    if 'Doctor' not in u.role:
        return returnResponse(400, {'message': 'Invalid input, user is not a doctor',
                                    'status': 'error'})
    clinic = getClinic(eventBody['clinicId'])
    if clinic is not None:
        return returnResponse(400, {'message': 'Invalid input, clinic exists, please modify instead',
                                    'status': 'error',
                                    'clinic': clinic.toJson()})
    clinic = Clinic(eventBody['clinicId'], eventBody['name'], eventBody['email'], eventBody['address'], eventBody['country'])
    uploadClinic(clinic)
    clinic = getClinic(eventBody['clinicId'])
    return returnResponse(200, {'message': 'clinic created',
                                'status': 'success',
                                'clinic': clinic.toJson()})

def getUser(userId):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    userTable = dynamodb.Table(os.environ['TABLE_USER'])
    try:
        item = userTable.get_item(
            TableName=os.environ['TABLE_USER'],
            Key={
                'userId': userId
            }
        )
        if 'Item' not in item:
            return None
        return User(userId, [item['Item']['firstName'], item['Item']['lastName']], item['Item']['email'], item['Item']['Address'], item['Item']['Country'], item['Item']['UserRoles'])
    except ClientError as e:
        return returnResponse(400, e.response['Error']['Message']) 

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
        return Clinic(clinicId, item['Item']['clinicName'], item['Item']['email'] , item['Item']['Address'], item['Item']['Country'])
    except ClientError as e:
        return returnResponse(400, e.response['Error']['Message'])

def uploadClinic(clinic):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    clinicTable = dynamodb.Table(os.environ['TABLE_CLINIC'])
    try:
        clinicTable.put_item(
            Item=clinic.toDict()
        )
        return True
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