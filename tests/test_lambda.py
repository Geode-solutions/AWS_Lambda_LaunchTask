import json
import uuid
from ..lambda_function import config


def test_load_config():
    ORIGIN_GEODE_SOLUTIONS = "https://geode-solutions.com"
    PATH_WEBSITE_CREATE_BACKEND = "/website/createbackend"
    ID = str(uuid.uuid4()).replace("-", "")
    CONFIG = config.Config(ORIGIN_GEODE_SOLUTIONS, PATH_WEBSITE_CREATE_BACKEND, ID)

    assert type(CONFIG.API_URL) is str
    assert type(CONFIG.ASSIGN_PUBLIC_IP) is str
    assert type(CONFIG.CLUSTER_NAME) is str
    assert type(CONFIG.ENVIRONMENT_VARIABLES) is dict
    assert type(CONFIG.HEALTHCHECK_PORT) is int
    assert type(CONFIG.HEALTHCHECK_ROUTE) is str
    assert type(CONFIG.LISTENER_ARN) is str
    assert type(CONFIG.PING_ROUTE) is str
    assert type(CONFIG.ORIGINS) is str
    assert type(CONFIG.SECONDS_BETWEEN_TRIES) is float
    assert type(CONFIG.SECURITY_GROUP) is str
    assert type(CONFIG.SUBNET_ID) is str
    assert type(CONFIG.TASK_DEF_NAME) is str
    assert type(CONFIG.VPC_ID) is str


def test_make_lambda_return():
    STATUS_CODE_200 = 200
    STATUS_DESCRIPTION_200 = "200 OK"
    ORIGIN_GEODE_SOLUTIONS = "https://geode-solutions.com"
    PATH_WEBSITE_CREATE_BACKEND = "/website/createbackend"
    ID = str(uuid.uuid4()).replace("-", "")
    CONFIG = config.Config(ORIGIN_GEODE_SOLUTIONS, PATH_WEBSITE_CREATE_BACKEND, ID)

    lambda_return = config.make_lambda_return(
        CONFIG, STATUS_CODE_200, STATUS_DESCRIPTION_200
    )
    assert type(lambda_return) is dict
    assert lambda_return == {
        "statusCode": STATUS_CODE_200,
        "statusDescription": STATUS_DESCRIPTION_200,
        "isBase64Encoded": False,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": CONFIG.ORIGINS,
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
    }

    BODY = dict({"ID": 123456})
    lambda_return = config.make_lambda_return(
        CONFIG, STATUS_CODE_200, STATUS_DESCRIPTION_200, BODY
    )
    assert type(lambda_return) is dict
    assert (
        lambda_return
        == lambda_return
        == {
            "statusCode": STATUS_CODE_200,
            "statusDescription": STATUS_DESCRIPTION_200,
            "isBase64Encoded": False,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": CONFIG.ORIGINS,
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json",
            },
            "body": json.dumps(BODY),
        }
    )

    STATUS_CODE_403 = 403
    STATUS_DESCRIPTION_403 = "403 Forbidden"
    ORIGIN_EMPTY = ""
    BODY = {"error_message": "Domain not allowed!"}
    lambda_return = config.make_lambda_return(
        CONFIG, STATUS_CODE_403, STATUS_DESCRIPTION_403, BODY
    )
    assert type(lambda_return) is dict
    assert (
        lambda_return
        == lambda_return
        == {
            "statusCode": STATUS_CODE_403,
            "statusDescription": STATUS_DESCRIPTION_403,
            "isBase64Encoded": False,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": CONFIG.ORIGINS,
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json",
            },
            "body": json.dumps(BODY),
        }
    )
