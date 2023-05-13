import json
import re
import boto3
import boto3 as bt3
import copy
import base64

def lambda_handler(event, context):
    access_key_id = 'YOUR_ACCESS_KEY_ID'
    secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
    region = 'us-west-1'
    iot = boto3.client('iot',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    
    body = eval(base64.b64decode(event['body']).decode('utf-8'))
    thingname = body['thingname']
    try:
        response = iot.create_thing(
            thingName = thingname
        )
    except BaseException as error:
        error = str(error)
        return error
    else:
        return response
