def load_config(
        REQUEST_ORIGIN: str, REQUEST_PATH: str):

    print(f'{REQUEST_ORIGIN=}')
    print(f'{REQUEST_PATH=}')

    CONFIG = {}
    CONFIG_DICT = {
        'TOOLS':
            {
                'PROD':
                    {
                        'CLUSTER_NAME': 'C_Tools_Prod', 'HEALTHCHECK_ROUTE': '/healthcheck', 'TASK_DEF_NAME': 'TD_Tools_Prod', 'ORIGINS': 'https://geode-solutions.com', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f', 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'VPC_ID': 'vpc-0e58c4d6976fb2aac', 'SECONDS_BETWEEN_TRIES': 0.25, 'HEALTHCHECK_PORT': 5000, 'ASSIGN_PUBLIC_IP': 'ENABLED'
                    }, 'DEV':
                    {
                        'CLUSTER_NAME': 'C_Tools_Dev', 'HEALTHCHECK_ROUTE': '/healthcheck', 'TASK_DEF_NAME': 'TD_Tools_Dev', 'ORIGINS': 'https://next.geode-solutions.com', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f', 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'VPC_ID': 'vpc-0e58c4d6976fb2aac', 'SECONDS_BETWEEN_TRIES': 0.25, 'HEALTHCHECK_PORT': 5000, 'ASSIGN_PUBLIC_IP': 'ENABLED'
                    }
            }, 'SHARETWIN':
            {
                'PROD':
                    {
                        'CLUSTER_NAME': 'C_ShareTwin_Prod', 'HEALTHCHECK_ROUTE': '/healthcheck', 'TASK_DEF_NAME': 'TD_ShareTwin_Prod', 'ORIGINS': 'https://share_twin.app', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4', 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'VPC_ID': 'vpc-0e58c4d6976fb2aac', 'SECONDS_BETWEEN_TRIES': 0.25, 'HEALTHCHECK_PORT': 5000, 'ASSIGN_PUBLIC_IP': 'ENABLED'
                    }, 'DEV':
                    {
                        'CLUSTER_NAME': 'C_ShareTwin_Dev', 'HEALTHCHECK_ROUTE': '/healthcheck', 'TASK_DEF_NAME': 'TD_ShareTwin_Dev', 'ORIGINS': 'https://friendly-dolphin-d9fdd1.netlify.app/', 'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4', 'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26', 'SUBNET_ID': 'subnet-0882d674b17515f6a', 'VPC_ID': 'vpc-0e58c4d6976fb2aac', 'SECONDS_BETWEEN_TRIES': 0.25, 'HEALTHCHECK_PORT': 5000, 'ASSIGN_PUBLIC_IP': 'ENABLED'
                    }
            }
    }

    if '/tools/' in REQUEST_PATH:
        CONFIG_TYPE = 'TOOLS'
        if REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['PROD']['ORIGINS']:
            CONFIG_ENV = 'PROD'
        elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['DEV']['ORIGINS']:
            CONFIG_ENV = 'DEV'
        else:
            return make_lambda_return(403, '403 Forbidden', '', {
                'error_message': 'Domain not allowed!'})
    elif '/sharetwin/' in REQUEST_PATH:
        CONFIG_TYPE = 'SHARETWIN'
        if REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['PROD']['ORIGINS']:
            CONFIG_TYPE = 'PROD'
        elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]['DEV']['ORIGINS']:
            CONFIG_TYPE = 'DEV'
        else:
            return make_lambda_return(403, '403 Forbidden', REQUEST_ORIGIN, {
                'error_message': 'Domain not allowed!'})

    CONFIG['CLUSTER_NAME'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['CLUSTER_NAME']
    CONFIG['HEALTHCHECK_PORT'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['HEALTHCHECK_PORT']
    CONFIG['HEALTHCHECK_ROUTE'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['HEALTHCHECK_ROUTE']
    CONFIG['LISTENER_ARN'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['LISTENER_ARN']
    CONFIG['ORIGINS'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['ORIGINS']
    CONFIG['SECONDS_BETWEEN_TRIES'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SECONDS_BETWEEN_TRIES']
    CONFIG['SECURITY_GROUP'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SECURITY_GROUP']
    CONFIG['SUBNET_ID'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['SUBNET_ID']
    CONFIG['TASK_DEF_NAME'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['TASK_DEF_NAME']
    CONFIG['VPC_ID'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['VPC_ID']

    return CONFIG


def make_lambda_return(STATUS_CODE: int, STATUS_DESCRIPTION: str, ORIGIN: str, BODY: dict = None):

    lamdba_return = dict([
        ('statusCode', STATUS_CODE), ('statusDescription', STATUS_DESCRIPTION), ('isBase64Encoded', False), ('headers', dict([
            ('Access-Control-Allow-Headers', 'Content-Type'), ('Access-Control-Allow-Origin',
                                                               ORIGIN), ('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
        ])
        )
    ])

    if BODY is not None:
        lamdba_return.update({'body': {}})
        for key in BODY:
            lamdba_return['body'][key] = BODY[key]

    return lamdba_return
