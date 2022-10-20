import json
import logging
import os
import boto3
import botocore
import urllib3
import uuid
import time

import functions
import config_functions


def lambda_handler(event, context):

    print('event :', event)

    if 'origin' in event:
        REQUEST_ORIGIN = event['origin']
    else:
        REQUEST_ORIGIN = ''

    REQUEST_PATH = event['path']
    HTTP_METHOD = event['httpMethod']

    CONFIG = config_functions.load_config(REQUEST_ORIGIN, REQUEST_PATH)
    print('CONFIG :', CONFIG)

    try:
        if HTTP_METHOD == 'OPTIONS':
            return config_functions.make_lambda_return(200, '200 OK', CONFIG['ORIGINS'])
        else:
            elbv2_client = boto3.client('elbv2')
            ecs_client = boto3.client('ecs')
            ID = str(uuid.uuid4()).replace('-', '')
            print('ID : ', ID)

            TaskArn = functions.create_fargate_task(ecs_client, ID)
            TargetGroupArn = functions.create_target_group(elbv2_client, ID)
            functions.addTag(ecs_client, TaskArn,
                             'TargetGroupArn', TargetGroupArn)
            RuleArn = functions.create_listener_rule(
                elbv2_client, ID, TargetGroupArn, 0)
            functions.addTag(ecs_client, TaskArn, 'RuleArn', RuleArn)
            FargatePrivateIP = functions.waitTaskAttached(
                ecs_client, TaskArn, 100)
            functions.waitForTaskRunning(
                ecs_client, FARGATE_CLUSTER, TaskArn, 150)
            Target = functions.create_target(
                elbv2_client, TargetGroupArn, FargatePrivateIP)
            functions.waitTargetHealthy(
                elbv2_client, TargetGroupArn, FargatePrivateIP, 100)
            functions.modifyTargetGroup(elbv2_client, TargetGroupArn)
            functions.waitForTaskResponding(ID, 100)

            return config_functions.make_lambda_return(200, '200 OK', ORIGIN, {'ID': ID})

    except Exception as e:
        print(e)
        return config_functions.make_lambda_return(500, '500 NOT OK', ORIGIN, {'error_message': str(e)})
