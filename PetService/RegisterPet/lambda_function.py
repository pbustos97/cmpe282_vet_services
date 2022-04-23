import json
import logging
import boto3
import os
from User import User
from Pet import Pet
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
        return returnResponse(400, {'message': 'Invalid input, no body',
                                    'status': 'error'})
    
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)
        logger.debug('[EVENT] eventBody: {}'.format(eventBody))
    
    if 'pet' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no user',
                                    'status': 'error'})
    eventBody = eventBody['pet']
    if type(eventBody) == str:
        eventBody = json.loads(eventBody)
    logger.debug('[EVENT] eventBody: {}'.format(eventBody))

    if 'name' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no name',
                                    'status': 'error'})
    if 'age' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no age',
                                    'status': 'error'})
    if 'ownerId' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no ownerId',
                                    'status': 'error'})
    if 'petId' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no petId',
                                    'status': 'error'})
    if 'breed' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no breed',
                                    'status': 'error'})
    if 'species' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no species',
                                    'status': 'error'})
    if 'weight' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no weight',
                                    'status': 'error'})

    pet = Pet(eventBody['name'], eventBody['age'], eventBody['ownerId'], eventBody['petId'], eventBody['breed'], eventBody['species'], eventBody['weight'])
    try:
        uploadPet(pet)
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return returnResponse(500, {'message': 'Error uploading pet', "status": "error", "error": e.response['Error']['Message']})
    
    return returnResponse(200, {'message': 'User created',
                                'pet': pet.toDict(),
                                'status': 'success'})

def uploadPet(pet):
    logger.debug('[UPLOAD] user: {}'.format(json.dumps(pet.toJson())))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    try:
        table.put_item(Item=pet.toDict())
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return returnResponse(500, {'message': 'Error uploading pet',"status": "error"})

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