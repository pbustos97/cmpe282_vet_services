import json
import logging
import boto3
import os
from Doctor import Doctor
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    logger.debug('[EVENT] eventType: {}'.format(type(event)))
    # Required since we want a unified input event
    eventBody = event
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)

    if 'queryStringParameters' in eventBody:
        eventBody = eventBody['queryStringParameters']
    else:
        return returnResponse(400, {'message': 'Invalid input, no queryStringParameters'})
    
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)
        logger.debug('[EVENT] queryStringParameters: {}'.format(eventBody))
    
    if 'doctorId' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no doctorId'})
    doctorId = eventBody['doctorId']
    try:
        doctor = getDoctor(doctorId)
        if (doctor == None):
            return returnResponse(400, {'message': 'Doctor does not exist'})
        doctor = Doctor(doctor['userId'], doctor['email'], doctor['ClinicId'], doctor['Speciality'])
        user = getUser(doctorId)
        if (user != None and doctor == None):
            return returnResponse(400, {'message': 'User is not a doctor'})
        if (user == None and doctor == None):
            return returnResponse(400, {'message': 'User does not exist'})
        return returnResponse(200, {'message': 'Retrieved Doctor',
                            'doctor': doctor.toDict(),
                            'user': {
                                'userId': user['userId'],
                                'email': user['email'],
                                'firstName': user['firstName'],
                                'lastName': user['lastName']
                            }})
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return returnResponse(500, {'message': 'Error getting doctor'})

def getDoctor(doctorId):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_DOCTOR'])
    try:
        response = table.get_item(
            Key={
                'userId': doctorId
            }
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e
    if 'Item' in response:
        return response['Item']
    return None

def getUser(userId):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_USER'])
    try:
        response = table.get_item(
            Key={
                'userId': userId
            }
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e
    if 'Item' in response:
        return {'userId': response['Item']['userId'], 'email': response['Item']['email'], 'firstName': response['Item']['firstName'], 'lastName': response['Item']['lastName']}
    return None

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