import functions

def load_config(
        REQUEST_ORIGIN: str
        , REQUEST_PATH: str):

    CONFIG = {
        'SECURITY_GROUP': 'sg-06cb4bf993f4ccb26'
        , 'SUBNET_ID': 'subnet-0882d674b17515f6a'
        , 'VPC_ID': 'vpc-0e58c4d6976fb2aac'
        , 'SECONDS_BETWEEN_TRIES': 0.25
        , 'HEALTHCHECK_PORT': 5000
        , 'TOOLS_CONFIG':
            {
                'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f'
                , 'TOOLS_PROD_CONFIG':
                    {
                        'CLUSTER_NAME': 'Tool_Prod'
                        , 'TASK_DEF_NAME': 'Tool_Prod'
                        , 'ORIGINS': 'https://geode-solutions.com'
                    }
                , 'TOOLS_DEV_CONFIG':
                    {
                        'CLUSTER_NAME': 'Tool_Dev'
                        , 'TASK_DEF_NAME': 'Tool_Dev'
                        , 'ORIGINS': 'https://geode-solutions.com'
                    }
            }
        , 'SHARETWIN_CONFIG':
            {
                'LISTENER_ARN': 'arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4'
                , 'SHARETWIN_PROD_CONFIG':
                    {
                        'CLUSTER_NAME': 'ShareTwin_Prod'
                        , 'TASK_DEF_NAME': 'ShareTwin_Prod'
                        , 'ORIGINS': 'https://share_twin.app'
                    }
                , 'SHARETWIN_DEV_CONFIG':
                    {
                        'CLUSTER_NAME': 'ShareTwin_Dev'
                        , 'TASK_DEF_NAME': 'ShareTwin_Dev'
                        , 'ORIGINS': 'https://friendly-dolphin-d9fdd1.netlify.app/'
                    }
            }
    }

    SECURITY_GROUP = CONFIG['SECURITY_GROUP']
    SUBNET_ID = CONFIG['SUBNET_ID']
    VPC_ID = CONFIG['VPC_ID']
    SECONDS_BETWEEN_TRIES = CONFIG['SECONDS_BETWEEN_TRIES']
    HEALTHCHECK_PORT = CONFIG['HEALTHCHECK_PORT']
    VPC_ID = CONFIG['VPC_ID']
    
    if '/tools/' in REQUEST_PATH:
        LISTENER_ARN = CONFIG['TOOLS_CONFIG']['LISTENER_ARN']
        if REQUEST_ORIGIN == 'https://geode-solutions.com':
            CONFIG_TYPE = 'TOOLS_PROD_CONFIG'
        elif REQUEST_ORIGIN == 'https://next.geode-solutions.com':
            CONFIG_TYPE = 'TOOLS_DEV_CONFIG'
        else:
            raise functions.make_lambda_return(403, '403 Forbidden', '', {'error_message': 'Domain not allowed!'})
            
        CLUSTER_NAME = CONFIG['TOOLS_CONFIG'][CONFIG_TYPE]['CLUSTER_NAME']
        TASK_DEF_NAME = CONFIG['TOOLS_CONFIG'][CONFIG_TYPE]['TASK_DEF_NAME']
        ORIGINS = CONFIG['TOOLS_CONFIG'][CONFIG_TYPE]['ORIGINS']
    elif '/sharetwin/' in REQUEST_PATH:
        LISTENER_ARN = CONFIG['TOOLS_CONFIG']['LISTENER_ARN']
        if REQUEST_ORIGIN == 'https://geode-solutions.com':
            CONFIG_TYPE = 'SHARETWIN_PROD_CONFIG'
        elif REQUEST_ORIGIN == 'https://next.geode-solutions.com':
            CONFIG_TYPE = 'SHARETWIN_DEV_CONFIG'
        else:
            raise functions.make_lambda_return(403, '403 Forbidden', '', {'error_message': 'Domain not allowed!'})

        CLUSTER_NAME = CONFIG['SHARETWIN_CONFIG'][CONFIG_TYPE]['CLUSTER_NAME']
        TASK_DEF_NAME = CONFIG['SHARETWIN_CONFIG'][CONFIG_TYPE]['TASK_DEF_NAME']
        ORIGINS = CONFIG['SHARETWIN_CONFIG'][CONFIG_TYPE]['ORIGINS']

    return

