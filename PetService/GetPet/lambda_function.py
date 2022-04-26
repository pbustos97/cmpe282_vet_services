import json
import logging
import boto3
import os
from Pet import Pet
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

    if 'queryStringParameters' in eventBody:
        eventBody = eventBody['queryStringParameters']
    else:
        return returnResponse(400, {'message': 'Invalid input, no body',
                                     'status': 'error'})
    
    if 'userId' not in eventBody: 
        return returnResponse(400, {'message': 'Invalid input, no user',
                                     'status': 'error'})
    user = getUser(eventBody['userId'])
    if user == None:
        return returnResponse(400, {'message': 'Invalid userId, user does not exist',
                                     'status': 'error'})

    if 'petId' not in eventBody:
        return returnResponse(400, {'message': 'Invalid input, no pet',
                                     'status': 'error'})
    if eventBody['petId'] == '-1':
        pets = getAllPets(eventBody['userId'])
        if pets == None:
            return returnResponse(400, {'message': 'Invalid userId, no pets',
                                         'status': 'error'})
        return returnResponse(200, {'message': 'All pets',
                                     'status': 'success',
                                     'pets': pets})

    pet = getPet(eventBody['petId'], eventBody['userId'])
    if pet == None:
        return returnResponse(400, {'message': 'Invalid petId, pet does not exist',
                                     'status': 'error'})

    return returnResponse(200, {'pet': pet.toJson(), 'status': 'success'})

def getUser(userId):
    logger.debug('[USER] userId: {}'.format(userId))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_USER'])
    try:
        response = table.get_item(
            Key={
                'userId': userId
            }
        )
        if 'Item' not in response:
            return None
        item = response['Item']
        logger.debug('[USER] item: {}'.format(item))
        user = User(item['userId'], [item['firstName'], item['lastName']], item['email'], item['Address'], item['Country'], item['UserRoles'])
        return user
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e

def getPet(petId, ownerId):
    logger.debug('[PET] petId: {}'.format(petId))
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
    userTable = dynamodb.Table(os.environ['TABLE_PET'])
    try:
        item = userTable.get_item(
            TableName=os.environ['TABLE_PET'],
            Key={
                'userId': ownerId,
                'petId': petId
            }
        )
        if 'Item' not in item:
            return None
        return Pet(item['Item']['PetName'], item['Item']['PetAge'], item['Item']['userId'], item['Item']['petId'], item['Item']['PetBreed'], item['Item']['PetSpecies'], item['Item']['PetWeight'])
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e
    
def getAllPets(ownerId):
    logger.debug('[PET] ownerId: {}'.format(ownerId))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_PET'])
    try:
        item = table.scan(
            ProjectionExpression = "userId, petId"
        )
        if 'Items' not in item:
            return None
        return item['Items']
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise e

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