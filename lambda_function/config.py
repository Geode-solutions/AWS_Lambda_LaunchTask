import json


class Config:
    def __init__(self, REQUEST_ORIGIN: str, REQUEST_PATH: str, ID: str = None):

        print(f'{REQUEST_ORIGIN=}')
        print(f'{REQUEST_PATH=}')

        CONFIG_DICT = {
            'TOOLS':
                {
                    'PROD':
                        {
                            'API_URL': 'https://api.geode-solutions.com',
                            'ASSIGN_PUBLIC_IP': 'ENABLED', 'CLUSTER_NAME': 'C_Tools_Prod', 'ENVIRONMENT_VARIABLES': {
                                'name': 'ToolsContainer', 'environment': [{'name': 'ID', 'value': ID}]
                            }, 'HEALTHCHECK_PORT': 5000, 'HEALTHCHECK_ROUTE': f'/{ID}/healthcheck', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f', 'NUMBER_OF_TRIES_TARGET_HEALTHY': 100, 'NUMBER_OF_TRIES_TASK_ATTACHED': 50, 'NUMBER_OF_TRIES_TASK_RESPONDING': 100, 'NUMBER_OF_TRIES_TASK_RUNNING': 100, 'ORIGINS': 'https://geode-solutions.com',
                            'PING_ROUTE': f'/{ID}/ping',
                            'SECONDS_BETWEEN_TRIES': 0.25, 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'TASK_DEF_NAME': 'TD_Tools_Prod', 'VPC_ID': 'vpc-0e58c4d6976fb2aac'
                        }, 'DEV':
                        {
                            'API_URL': 'https://api.geode-solutions.com',
                            'ASSIGN_PUBLIC_IP': 'ENABLED', 'CLUSTER_NAME': 'C_Tools_Dev', 'ENVIRONMENT_VARIABLES': {
                                'name': 'ToolsContainer', 'environment': [{'name': 'ID', 'value': ID}]
                            }, 'HEALTHCHECK_PORT': 5000, 'HEALTHCHECK_ROUTE': f'/{ID}/healthcheck', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f', 'NUMBER_OF_TRIES_TARGET_HEALTHY': 100, 'NUMBER_OF_TRIES_TASK_ATTACHED': 50, 'NUMBER_OF_TRIES_TASK_RESPONDING': 100, 'NUMBER_OF_TRIES_TASK_RUNNING': 100, 'ORIGINS': 'https://next.geode-solutions.com',
                            'PING_ROUTE': f'/{ID}/ping','SECONDS_BETWEEN_TRIES': 0.25, 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'TASK_DEF_NAME': 'TD_Tools_Dev', 'VPC_ID': 'vpc-0e58c4d6976fb2aac'
                        }
                }, 'SHARETWIN':
                {
                    'PROD':
                        {
                            'API_URL': 'https://api2.geode-solutions.com',
                            'ASSIGN_PUBLIC_IP': 'ENABLED', 'CLUSTER_NAME': 'C_ShareTwin_Prod', 'ENVIRONMENT_VARIABLES': {
                                'name': 'GeodeBackEnd', 'environment': [{
                                    'name': 'ID', 'value': ID}]
                            }, 'HEALTHCHECK_PORT': 443, 'HEALTHCHECK_ROUTE': f'/{ID}/geode/healthcheck', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4', 'NUMBER_OF_TRIES_TARGET_HEALTHY': 1000, 'NUMBER_OF_TRIES_TASK_ATTACHED': 50, 'NUMBER_OF_TRIES_TASK_RESPONDING': 1000, 'NUMBER_OF_TRIES_TASK_RUNNING': 500,
                            'PING_ROUTE': f'/{ID}/geode/ping',
                            'ORIGINS': 'https://share-twin.com', 'SECONDS_BETWEEN_TRIES': 0.25, 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'TASK_DEF_NAME': 'TD_ShareTwin_Prod', 'VPC_ID': 'vpc-0e58c4d6976fb2aac'
                        }, 'DEV':
                        {
                            'API_URL': 'https://api2.geode-solutions.com',
                            'ASSIGN_PUBLIC_IP': 'ENABLED', 'CLUSTER_NAME': 'C_ShareTwin_Dev', 'ENVIRONMENT_VARIABLES': {
                                'name': 'GeodeBackEnd', 'environment': [{
                                    'name': 'ID', 'value': ID}]
                            }, 'HEALTHCHECK_PORT': 443, 'HEALTHCHECK_ROUTE': f'/{ID}/geode/healthcheck', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4', 'NUMBER_OF_TRIES_TARGET_HEALTHY': 1000, 'NUMBER_OF_TRIES_TASK_ATTACHED': 50, 'NUMBER_OF_TRIES_TASK_RESPONDING': 1000, 'NUMBER_OF_TRIES_TASK_RUNNING': 500,
                            'PING_ROUTE': f'/{ID}/geode/ping',
                            'ORIGINS': 'https://friendly-dolphin-d9fdd1.netlify.app/', 'SECONDS_BETWEEN_TRIES': 0.25, 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'TASK_DEF_NAME': 'TD_ShareTwin_Dev', 'VPC_ID': 'vpc-0e58c4d6976fb2aac'
                        }
                }
        }

        if '/tools/' in REQUEST_PATH:
            CONFIG_TYPE = 'TOOLS'
            if REQUEST_ORIGIN == '':
                CONFIG_TYPE = 'DEV'
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['PROD']['ORIGINS']:
                CONFIG_ENV = 'PROD'
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['DEV']['ORIGINS']:
                CONFIG_ENV = 'DEV'
        elif '/sharetwin/' in REQUEST_PATH:
            CONFIG_TYPE = 'SHARETWIN'
            if REQUEST_ORIGIN == '':
                CONFIG_TYPE = 'DEV'
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['PROD']['ORIGINS']:
                CONFIG_ENV = 'PROD'
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['DEV']['ORIGINS']:
                CONFIG_ENV = 'DEV'

        self.API_URL = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['API_URL']
        self.ASSIGN_PUBLIC_IP = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['ASSIGN_PUBLIC_IP']
        self.CLUSTER_NAME = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['CLUSTER_NAME']
        self.ENVIRONMENT_VARIABLES = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['ENVIRONMENT_VARIABLES']
        self.HEALTHCHECK_PORT = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['HEALTHCHECK_PORT']
        self.HEALTHCHECK_ROUTE = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['HEALTHCHECK_ROUTE']
        self.LISTENER_ARN = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['LISTENER_ARN']
        self.NUMBER_OF_TRIES_TARGET_HEALTHY = CONFIG_DICT[
            CONFIG_TYPE][CONFIG_ENV]['NUMBER_OF_TRIES_TARGET_HEALTHY']
        self.NUMBER_OF_TRIES_TASK_ATTACHED = CONFIG_DICT[
            CONFIG_TYPE][CONFIG_ENV]['NUMBER_OF_TRIES_TASK_ATTACHED']
        self.NUMBER_OF_TRIES_TASK_RESPONDING = CONFIG_DICT[
            CONFIG_TYPE][CONFIG_ENV]['NUMBER_OF_TRIES_TASK_RESPONDING']
        self.NUMBER_OF_TRIES_TASK_RUNNING = CONFIG_DICT[
            CONFIG_TYPE][CONFIG_ENV]['NUMBER_OF_TRIES_TASK_RUNNING']
        self.PING_ROUTE = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['PING_ROUTE']
        self.ORIGINS = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['ORIGINS']
        self.SECONDS_BETWEEN_TRIES = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SECONDS_BETWEEN_TRIES']
        self.SECURITY_GROUP = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SECURITY_GROUP']
        self.SUBNET_ID = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SUBNET_ID']
        self.TASK_DEF_NAME = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['TASK_DEF_NAME']
        self.VPC_ID = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['VPC_ID']


def make_lambda_return(CONFIG, STATUS_CODE: int, STATUS_DESCRIPTION: str, BODY: dict = None):

    lamdba_return = dict([
        ('statusCode', STATUS_CODE), ('statusDescription', STATUS_DESCRIPTION), ('isBase64Encoded', False), ('headers', dict([
            ('Access-Control-Allow-Headers', 'Content-Type'), ('Access-Control-Allow-Origin',
                                                               getattr(CONFIG, 'ORIGINS')), ('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
        ])
        )
    ])

    if BODY is not None:
        lamdba_return['body'] = json.dumps(BODY)
    return lamdba_return
