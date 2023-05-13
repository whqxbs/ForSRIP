import json
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
    setasactive = body['setasactive']
    if setasactive == 'True' or setasactive == 'true':
        setasactive = True
    elif setasactive == 'False' or setasactive == 'false':
        setasactive = False
    try:
        response = iot.create_keys_and_certificate(
            setAsActive = setasactive
        )
    except BaseException as error:
        error = str(error)
        return error
    else:
        return response