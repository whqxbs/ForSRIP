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
    
    dynamodb = boto3.client('dynamodb',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    iot = boto3.client('iot',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
    
    body = eval(base64.b64decode(event['body']).decode('utf-8'))
    policy_name = body['name']
    policy_json = body['json']
    policy_type = body['type']
    vd_db = body['V_D']
    vu_db = body['V_U']
    column_vtagd = body['C_V_TAG_d']
    column_vtagu = body['C_V_TAG_u']
    column_userid = body['C_user_id']
    column_deviceid = body['C_device_id']
    
    if policy_type not in [1, 2]:
        return {
        'statusCode': 400,
        'body': 'Policy Type Error!'
        }
    
    if policy_name == '':
        return {
        'statusCode': 400,
        'body': 'Policy Name Error!'
        }
        
    if policy_json == '':
        return {
        'statusCode': 400,
        'body': 'Policy Json Error!'
        }
    
    if policy_type == 1:
        response = iot.create_policy(policyName = policy_name, policyDocument = policy_json)
        return response
    
    if policy_type == 2:
        if vd_db == '' or vu_db == '' or column_vtagd == '' or column_vtagu == '' or column_userid == '' or column_deviceid == '':
            return {
            'statusCode': 400,
            'body': 'DynamoDB Information Error!'
            }
        
        policy_variable = re.findall(r'\${(.*?)}', policy_json, re.S)
        policy_variable_mid = re.findall(r'\${.*?}', policy_json, re.S)
        
        flag = 0
        mid_json = policy_json
        
        for item in policy_variable:
            res_tag = dynamodb.execute_statement(Statement="""SELECT "{}" FROM "{}" WHERE "{}" = '{}'""".format(column_vtagu, vu_db, column_userid, item))
            res_device_id = dynamodb.execute_statement(Statement="""SELECT "{}" FROM "{}" WHERE "{}" = '{}'""".format(column_deviceid, vd_db, column_vtagd, res_tag['Items'][0][column_vtagd]['S']))
            device_id = res_device_id['Items'][0][column_deviceid]['S']
            #print(device_id)
            mid_json = mid_json.replace(policy_variable_mid[flag], device_id)
            flag = flag + 1
        policy_json = mid_json
        response = iot.create_policy(policyName = policy_name, policyDocument = policy_json)
        return response