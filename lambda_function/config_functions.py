def load_config(
        REQUEST_ORIGIN: str, REQUEST_PATH: str):

    CONFIG = {}
    CONFIG['SECURITY_GROUP'] = 'sg-06cb4bf993f4ccb26'
    CONFIG['SUBNET_ID'] = 'subnet-0882d674b17515f6a'
    CONFIG['VPC_ID'] = 'vpc-0e58c4d6976fb2aac'
    CONFIG['SECONDS_BETWEEN_TRIES'] = 0.25
    CONFIG['HEALTHCHECK_PORT'] = 5000

    CONFIG_DICT = {
        'TOOLS':
            {
                'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f', 'PROD':
                    {
                        'CLUSTER_NAME': 'Tool_Prod', 'TASK_DEF_NAME': 'Tool_Prod', 'ORIGINS': 'https://geode-solutions.com'
                    }, 'DEV':
                    {
                        'CLUSTER_NAME': 'Tool_Dev', 'TASK_DEF_NAME': 'Tool_Dev', 'ORIGINS': 'https://geode-solutions.com'
                    }
            }, 'SHARETWIN':
            {
                'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4', 'PROD':
                    {
                        'CLUSTER_NAME': 'ShareTwin_Prod', 'TASK_DEF_NAME': 'ShareTwin_Prod', 'ORIGINS': 'https://share_twin.app'
                    }, 'DEV':
                    {
                        'CLUSTER_NAME': 'ShareTwin_Dev', 'TASK_DEF_NAME': 'ShareTwin_Dev', 'ORIGINS': 'https://friendly-dolphin-d9fdd1.netlify.app/'
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

    CONFIG['LISTENER_ARN'] = CONFIG_DICT[CONFIG_TYPE]['LISTENER_ARN']
    CONFIG['CLUSTER_NAME'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['CLUSTER_NAME']
    CONFIG['TASK_DEF_NAME'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['TASK_DEF_NAME']
    CONFIG['ORIGINS'] = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]['ORIGINS']
    return CONFIG


def make_lambda_return(STATUS_CODE: int, STATUS_DESCRIPTION: str, ORIGIN: str, BODY: dict = None):

    lamdba_return = dict([
        ('statusCode', STATUS_CODE), ('statusDescription', STATUS_DESCRIPTION), ('isBase64Encoded', False), ('headers', dict([
            ('Access-Control-Allow-Headers', 'Content-Type'), ('Access-Control-Allow-Origin',
                                                               ORIGIN), ('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
        ])
        )
    ])

    print(type(lamdba_return))

    if BODY is not None:
        lamdba_return.update({'body': {}})
        for key in BODY:
            lamdba_return['body'][key] = BODY[key]

    return lamdba_return
