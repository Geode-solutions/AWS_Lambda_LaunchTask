import json
import logging
import os
import boto3
import botocore
import urllib3
import uuid
import time
import threading


def create_fargate_task(CONFIG, ecs_client: botocore.client, ID: str):

    fargate = ecs_client.run_task(
        cluster=getattr(CONFIG, 'CLUSTER_NAME'),
        count=1,
        launchType='FARGATE',
        taskDefinition=getattr(CONFIG, 'TASK_DEF_NAME'),
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    getattr(CONFIG, 'SUBNET_ID'),
                ],
                'securityGroups': [getattr(CONFIG, 'SECURITY_GROUP')],
                'assignPublicIp': getattr(CONFIG, 'ASSIGN_PUBLIC_IP')
            }
        },
        overrides={'containerOverrides': [
            getattr(CONFIG, 'ENVIRONMENT_VARIABLES')]},
    )

    failures = fargate['failures']
    if failures:
        print(f'{failures=}')
        taskArn = create_fargate_task(ecs_client, ID)
    else:
        taskArn = fargate['tasks'][0]['taskArn']

    return taskArn


def create_target_group(CONFIG, elbv2_client: botocore.client,
                        ID: str):

    targetGroup = elbv2_client.create_target_group(
        Name=ID,
        Protocol='HTTPS',
        ProtocolVersion='HTTP1',
        Port=443,
        VpcId=getattr(CONFIG, 'VPC_ID'),
        HealthCheckProtocol='HTTPS',
        HealthCheckPort='traffic-port',
        HealthCheckEnabled=True,
        HealthCheckPath=getattr(CONFIG, 'HEALTHCHECK_ROUTE'),
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


def create_listener_rule(CONFIG,
                         elbv2_client: botocore.client,
                         ID: str,
                         targetGroupArn: str,
                         RulesCountAdd: int = 0):
    ListenerRules = elbv2_client.describe_rules(
        ListenerArn=getattr(CONFIG, 'LISTENER_ARN'))
    RulesCount = len(ListenerRules['Rules']) + 1 + RulesCountAdd

    try:
        listenerRule = elbv2_client.create_rule(
            ListenerArn=getattr(CONFIG, 'LISTENER_ARN'),
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
        return create_listener_rule(CONFIG, elbv2_client, ID, targetGroupArn, RulesCountAdd + 1)

    RuleArn = listenerRule['Rules'][0]['RuleArn']
    return RuleArn


def register_target(CONFIG,
                    elbv2_client: botocore.client,
                    targetGroupArn: str,
                    fargatePrivateIP: str):
    target = elbv2_client.register_targets(
        TargetGroupArn=targetGroupArn,
        Targets=[
            {
                'Id': fargatePrivateIP,
                'Port': getattr(CONFIG, 'HEALTHCHECK_PORT')
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


def waitTaskAttached(CONFIG,
                     ecs_client: botocore.client,
                     taskArn: str):
    print('Wait task attached')
    taskStatus = ''

    while taskStatus != 'ATTACHED':
        taskDescription = ecs_client.describe_tasks(
            cluster=CONFIG.CLUSTER_NAME,
            tasks=[taskArn]
        )
        taskStatus = taskDescription['tasks'][0]['attachments'][0]['status']

        if taskStatus == 'ATTACHED':
            break
        elif taskStatus == 'DETACHING' or taskStatus == 'DETACHED' or taskStatus == 'DELETED' or taskStatus == 'FAILED':
            print(f'{taskStatus=}')
            raise Exception('Task not attached')
        else:
            time.sleep(CONFIG.SECONDS_BETWEEN_TRIES)
    print('Task attached !')
    FargatePrivateIP = taskDescription['tasks'][0]['attachments'][0]['details'][4]['value']
    return FargatePrivateIP


def waitTargetHealthy(CONFIG,
                      elbv2_client: botocore.client,
                      TargetGroupArn: str,
                      FargatePrivateIP: str):
    print('Wait target healthy')
    targetHealthStatus = ''
    while targetHealthStatus != 'healthy':
        targetHealthDescription = elbv2_client.describe_target_health(
            TargetGroupArn=TargetGroupArn,
            Targets=[
                {
                    'Id': FargatePrivateIP,
                    'Port': getattr(CONFIG, 'HEALTHCHECK_PORT')
                },
            ]
        )
        targetHealthStatus = targetHealthDescription['TargetHealthDescriptions'][0]['TargetHealth']['State']
        if targetHealthStatus == 'healthy':
            break
        if targetHealthStatus == 'unhealthy':
            raise Exception('Target unhealthy !')
        else:
            time.sleep(getattr(CONFIG, 'SECONDS_BETWEEN_TRIES'))
    print('Target healthy !')
    return


def modifyTargetGroup(elbv2_client: botocore.client,
                      TargetGroupArn: str):
    response = elbv2_client.modify_target_group(
        TargetGroupArn=TargetGroupArn,
        HealthCheckIntervalSeconds=5,
        HealthCheckTimeoutSeconds=2,
        HealthyThresholdCount=2,
        UnhealthyThresholdCount=2
    )


def waitForTaskRunning(CONFIG, ecs_client: botocore.client,
                       TaskArn: str):
    print('Wait task running')
    taskStatus = ''
    while taskStatus != 'RUNNING':
        taskDescription = ecs_client.describe_tasks(
            cluster=getattr(CONFIG, 'CLUSTER_NAME'), tasks=[TaskArn])
        taskStatus = taskDescription['tasks'][0]['lastStatus']
        if taskStatus == 'RUNNING':
            break
        elif taskStatus == 'DEACTIVATING' or taskStatus == 'STOPPING' or taskStatus == 'DEPROVISIONING' or taskStatus == 'STOPPED':
            print(f'{taskStatus=}')
            raise Exception('Task not running')
        else:
            time.sleep(getattr(CONFIG, 'SECONDS_BETWEEN_TRIES'))
    print('Task running !')
    return


def waitForTaskResponding(CONFIG,
                          ID: str):
    print('Wait task responding')
    API_URL = getattr(CONFIG, 'API_URL')
    PING_ROUTE = getattr(CONFIG, 'PING_ROUTE')
    print(f'{API_URL=}{PING_ROUTE=}')
    STATUS = 0

    while STATUS != 200:
        https = urllib3.PoolManager()
        r = https.request('POST', f'{API_URL}{PING_ROUTE}')
        STATUS = r.status
        if STATUS == 200:
            break
        elif STATUS == 404:
            raise Exception(f'{API_URL}{PING_ROUTE} doesn''t exist')
        elif r.status != 200:
            time.sleep(getattr(CONFIG, 'SECONDS_BETWEEN_TRIES'))
    print(f'{r.data=}')
    print('Task responded !')
    return


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t


def ping_task(CONFIG, fargate_private_ip):
    PING_ROUTE = getattr(CONFIG, 'PING_ROUTE')
    HEALTHCHECK_PORT = getattr(CONFIG, 'HEALTHCHECK_PORT')
    URL = f'https://{fargate_private_ip}:{HEALTHCHECK_PORT}{PING_ROUTE}'
    print(f'{URL=}')
    STATUS = 0

    while STATUS != 200:
        https = urllib3.PoolManager()
        r = https.request('POST', URL)
        STATUS = r.status
        if STATUS == 200:
            break
        elif STATUS == 404:
            raise Exception(f'{URL} doesn''t exist')
        elif r.status != 200:
            time.sleep(getattr(CONFIG, 'SECONDS_BETWEEN_TRIES'))
    print(f'{r.data=}')
    print('Task responded !')
    return
