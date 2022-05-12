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

    if 'body' in eventBody:
        eventBody = eventBody['body']
    else:
        return returnResponse(400, {'message': 'Invalid input, no body'})
    
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)
        logger.debug('[EVENT] eventBody: {}'.format(eventBody))
    
    if 'doctor' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no doctor'})

    if 'doctorId' not in eventBody['doctor']:
        return returnResponse(400, {'message': 'Invalid input, no doctorId'})
    if 'email' not in eventBody['doctor']:
        return returnResponse(400, {'message': 'Invalid input, no email'})
    if 'speciality' not in eventBody['doctor']:
        speciality = 'General'
    elif len(eventBody['doctor']['speciality']) == 0:
        return returnResponse(400, {'message': 'Invalid input, empty speciality'})
    else:
        speciality = eventBody['doctor']['speciality']

    doctor = Doctor(eventBody['doctor']['doctorId'], eventBody['doctor']['email'], speciality)
    try:
        if (getDoctor(doctor.doctorId) != None):
            return returnResponse(400, {'message': 'Doctor already exists'})
        uploadDoctor(doctor)
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return returnResponse(500, {'message': 'Error uploading user'})
    
    return returnResponse(200, {'message': 'User created',
                                'doctor': doctor.toJson()})

def uploadDoctor(doctor):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_DOCTOR'])
    try:
        response = table.put_item(
            Item=doctor.toDict()
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e
    return response

def getDoctor(doctorId):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_DOCTOR'])
    try:
        response = table.get_item(
            Key={
                'docterId': doctorId
            }
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e
    if 'Item' in response:
        return response['Item']
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