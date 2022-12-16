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


def lambda_handler(event, context):

    print(f'{event=}')

    if 'origin' in event['headers']:
        REQUEST_ORIGIN = event['headers']['origin']
    else:
        REQUEST_ORIGIN = ''

    REQUEST_PATH = event['path']
    HTTP_METHOD = event['httpMethod']
    ID = str(uuid.uuid4()).replace('-', '')

    CONFIG = config.Config(REQUEST_ORIGIN, REQUEST_PATH, ID)

    try:
        if HTTP_METHOD == 'OPTIONS':
            return config.make_lambda_return(CONFIG, 200, '200 OK')
        else:
            print(f'{ID=}')
            elbv2_client = boto3.client('elbv2')
            print(f'{ID=}')
            ecs_client = boto3.client('ecs')
            print(f'{ID=}')

            task_arn = functions.create_fargate_task(CONFIG, ecs_client, ID)
            print(f'{ID=}')
            target_group_arn = functions.create_target_group(
                CONFIG, elbv2_client, ID)
            functions.add_tag(ecs_client, task_arn,
                              'target_group_arn', target_group_arn)
            rule_arn = functions.create_listener_rule(
                CONFIG, elbv2_client, ID, target_group_arn, 0)
            functions.add_tag(ecs_client, task_arn, 'rule_arn', rule_arn)
            fargate_private_ip, fargate_public_ip = functions.wait_task_attached(
                CONFIG, ecs_client, task_arn)
            functions.wait_for_task_running(CONFIG, ecs_client, task_arn)
            functions.set_interval(functions.ping_task(
                CONFIG, fargate_public_ip), 10)
            Target = functions.register_target(
                CONFIG, elbv2_client, target_group_arn, fargate_private_ip)
            functions.wait_target_healthy(
                CONFIG, elbv2_client, target_group_arn, fargate_private_ip)
            functions.modify_target_group(elbv2_client, target_group_arn)
            functions.wait_for_task_responding(CONFIG, ID)

            return config.make_lambda_return(CONFIG, 200, '200 OK', {'ID': ID})

    except Exception as e:
        print(f'{str(e)=}')
        return config.make_lambda_return(CONFIG, 500, '500 NOT OK', {'error_message': str(e)})
