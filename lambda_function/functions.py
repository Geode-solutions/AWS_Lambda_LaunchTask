import json
import logging
import os
import boto3
import botocore
import urllib3
import uuid
import time

def create_fargate_task(config: config, ecs_client: botocore.client, ID: str):

    fargate = ecs_client.run_task(
        cluster=config.CLUSTER_NAME,
        count=1,
        launchType='FARGATE',
        taskDefinition=config.TASK_DEF_NAME,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    config.SUBNET_ID,
                ],
                'securityGroups': [config.SECURITY_GROUP],
                'assignPublicIp': config.ASSIGN_PUBLIC_IP
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': 'ToolsContainer',
                    'environment': [
                        {
                            'name': 'ID',
                            'value': ID
                        },
                        {
                            'name': 'FLASK_ENV',
                            'value': 'production',
                        },

                    ],
                },
            ],
        },
    )

    failures = fargate['failures']
    if failures:
        print(f'{failures=}')
        taskArn = create_fargate_task(ecs_client, ID)
    else:
        taskArn = fargate['tasks'][0]['taskArn']

    return taskArn


def create_target_group(config: config, elbv2_client: botocore.client,
                        ID: str):

    targetGroup = elbv2_client.create_target_group(
        Name=ID,
        Protocol='HTTPS',
        ProtocolVersion='HTTP1',
        Port=443,
        VpcId=config.VPC_ID,
        HealthCheckProtocol='HTTPS',
        HealthCheckPort='traffic-port',
        HealthCheckEnabled=True,
        HealthCheckPath=f'/{ID}{config.HEALTHCHECK_ROUTE}',
        HealthCheckIntervalSeconds=5,
        HealthCheckTimeoutSeconds=4,
        HealthyThresholdCount=2,
        UnhealthyThresholdCount=5,
        Matcher={
            'HttpCode': '200',
        },
        TargetType='ip'
    )

    targetGroupArn = targetGroup['TargetGroups'][0]['TargetGroupArn']
    return targetGroupArn


def create_listener_rule(elbv2_client: botocore.client,
                         ID: str,
                         targetGroupArn: str,
                         RulesCountAdd: int = 0):
    ListenerRules = elbv2_client.describe_rules(
        ListenerArn=config.LISTENER_ARN)
    RulesCount = len(ListenerRules['Rules']) + 1 + RulesCountAdd

    try:
        listenerRule = elbv2_client.create_rule(
            ListenerArn=config.LISTENER_ARN,
            Conditions=[
                {
                    'Field': 'path-pattern',
                    'Values': [
                        '/' + ID + '/*'
                    ],
                },
            ],
            Priority=RulesCount,
            Actions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': targetGroupArn,
                    'Order': 1,
                    'ForwardConfig': {
                        'TargetGroups': [
                            {
                                'TargetGroupArn': targetGroupArn,
                                'Weight': 1
                            },
                        ],
                    }
                },
            ],
        )

    except elbv2_client.exceptions.PriorityInUseException:
        print('Retrying create_rule :', RulesCountAdd)
        return create_listener_rule(elbv2_client, ID, targetGroupArn, RulesCountAdd + 1)

    RuleArn = listenerRule['Rules'][0]['RuleArn']
    return RuleArn


def register_target(config: config, elbv2_client: botocore.client,
                    targetGroupArn: str,
                    fargatePrivateIP: str):
    target = elbv2_client.register_targets(
        TargetGroupArn=targetGroupArn,
        Targets=[
            {
                'Id': fargatePrivateIP,
                'Port': config.HEALTHCHECK_PORT
            },
        ]
    )
    return target


def addTag(ecs_client: botocore.client,
           taskArn: str,
           key: str,
           value: str):
    response = ecs_client.tag_resource(
        resourceArn=taskArn,
        tags=[
            {
                'key': key,
                'value': value
            },
        ]
    )


def waitTaskAttached(config: config,
                     ecs_client: botocore.client,
                     taskArn: str,
                     numberOfTries: int):
    for tries in range(numberOfTries):
        taskDescription = ecs_client.describe_tasks(
            cluster=config.CLUSTER_NAME,
            tasks=[taskArn]
        )

        taskStatus = taskDescription['tasks'][0]['attachments'][0]['status']

        if taskStatus == 'ATTACHED':
            print('Task attached !')
            FargatePrivateIP = taskDescription['tasks'][0]['attachments'][0]['details'][4]['value']
            return FargatePrivateIP
        else:
            time.sleep(config.SECONDS_BETWEEN_TRIES)
    raise Exception('Task not attached')


def waitTargetHealthy(config: config,
                      elbv2_client: botocore.client,
                      TargetGroupArn: str,
                      FargatePrivateIP: str,
                      numberOfTries: int):
    for tries in range(numberOfTries):
        targetHealthDescription = elbv2_client.describe_target_health(
            TargetGroupArn=TargetGroupArn,
            Targets=[
                {
                    'Id': FargatePrivateIP,
                    'Port': config.HEALTHCHECK_PORT
                },
            ]
        )
        targetHealthStatus = targetHealthDescription['TargetHealthDescriptions'][0]['TargetHealth']['State']

        if targetHealthStatus == 'healthy':
            print('Target healthy !')
            return
        else:
            time.sleep(config.SECONDS_BETWEEN_TRIES)
    raise Exception('Target not healthy')


def modifyTargetGroup(config: config,
                      elbv2_client: botocore.client,
                      TargetGroupArn: str):
    response = elbv2_client.modify_target_group(
        TargetGroupArn=TargetGroupArn,
        HealthCheckIntervalSeconds=5,
        HealthCheckTimeoutSeconds=2,
        HealthyThresholdCount=2,
        UnhealthyThresholdCount=2
    )


def waitForTaskRunning(config: config, ecs_client: botocore.client,
                       TaskArn: str,
                       numberOfTries: int):

    for tries in range(numberOfTries):
        taskDescription = ecs_client.describe_tasks(
            cluster=config.CLUSTER_NAME, tasks=[TaskArn])
        taskStatus = taskDescription['tasks'][0]['lastStatus']

        if taskStatus == 'RUNNING':
            print('Task running !')
            return
        else:
            time.sleep(config.SECONDS_BETWEEN_TRIES)
    raise Exception('Task not running')


def waitForTaskResponding(config: config,
                          ID: str,
                          numberOfTries: int):
    for tries in range(numberOfTries):
        https = urllib3.PoolManager()
        r = https.request('POST', f'https://api.geode-solutions.com/{ID}/ping')
        if r.status != 200:
            print('Task didn''t respond')
            time.sleep(config.SECONDS_BETWEEN_TRIES)
        else:
            print('response : ', r.data)
            print('Task responded ! ')
            return

    raise Exception('Task not responding')
