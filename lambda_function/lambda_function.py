import json
import logging
import os
import boto3
import botocore
import urllib3
import uuid
import time

import config
import functions
import config_functions


def lambda_handler(event, context):

    print(f'{event=}')

    if 'origin' in event['headers']:
        REQUEST_ORIGIN = event['headers']['origin']
    else:
        REQUEST_ORIGIN = ''

    REQUEST_PATH = event['path']
    HTTP_METHOD = event['httpMethod']

    CONFIG = config.Config(REQUEST_ORIGIN, REQUEST_PATH)
    # print(str(CONFIG))

    try:
        if HTTP_METHOD == 'OPTIONS':
            return config_functions.make_lambda_return(200, '200 OK', getattr(CONFIG, 'ORIGINS'))
        else:
            elbv2_client = boto3.client('elbv2')
            ecs_client = boto3.client('ecs')
            ID = str(uuid.uuid4()).replace('-', '')
            print(f'{ID=}')

            TaskArn = functions.create_fargate_task(CONFIG, ecs_client, ID)
            TargetGroupArn = functions.create_target_group(
                CONFIG, elbv2_client, ID)
            functions.addTag(ecs_client, TaskArn,
                             'TargetGroupArn', TargetGroupArn)
            RuleArn = functions.create_listener_rule(
                CONFIG, elbv2_client, ID, TargetGroupArn, 0)
            functions.addTag(ecs_client, TaskArn, 'RuleArn', RuleArn)
            FargatePrivateIP = functions.waitTaskAttached(
                ecs_client, TaskArn, 100)
            functions.waitForTaskRunning(CONFIG,
                                         ecs_client, TaskArn, 150)
            Target = functions.register_target(
                elbv2_client, TargetGroupArn, FargatePrivateIP)
            functions.waitTargetHealthy(
                elbv2_client, TargetGroupArn, FargatePrivateIP, 100)
            functions.modifyTargetGroup(elbv2_client, TargetGroupArn)
            functions.waitForTaskResponding(CONFIG, ID, 100)

            return config_functions.make_lambda_return(200, '200 OK', getattr(CONFIG, 'ORIGINS'), {'ID': ID})

    except Exception as e:
        print(e)
        return config_functions.make_lambda_return(500, '500 NOT OK', getattr(CONFIG, 'ORIGINS'), {'error_message': str(e)})
