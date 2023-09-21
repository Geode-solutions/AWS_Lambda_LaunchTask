import json


class Config:
    def __init__(self, REQUEST_ORIGIN: str, REQUEST_PATH: str, ID: str = None):
        print(f"{REQUEST_ORIGIN=}")
        print(f"{REQUEST_PATH=}")

        CONFIG_DICT = {
            "WEBSITE": {
                "MASTER": {
                    "API_URL": "https://api.geode-solutions.com",
                    "ASSIGN_PUBLIC_IP": "ENABLED",
                    "CLUSTER_NAME": "C_Website_Master",
                    "ENVIRONMENT_VARIABLES": {
                        "name": "geode",
                        "environment": [{"name": "ID", "value": ID}],
                    },
                    "HEALTHCHECK_PORT": 443,
                    "HEALTHCHECK_ROUTE": f"/{ID}/geode/healthcheck",
                    "LISTENER_ARN": "arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f",
                    "ORIGINS": "https://geode-solutions.com",
                    "PING_ROUTE": f"/{ID}/geode/ping",
                    "SECONDS_BETWEEN_TRIES": 0.25,
                    "SECURITY_GROUP": "sg-0ef1a0691e5f59c23",
                    "SUBNET_ID": "subnet-0882d674b17515f6a",
                    "TASK_DEF_NAME": "TD_Website_Master",
                    "VPC_ID": "vpc-0e58c4d6976fb2aac",
                },
                "NEXT": {
                    "API_URL": "https://api.geode-solutions.com",
                    "ASSIGN_PUBLIC_IP": "ENABLED",
                    "CLUSTER_NAME": "C_Website_Next",
                    "ENVIRONMENT_VARIABLES": {
                        "name": "geode",
                        "environment": [{"name": "ID", "value": ID}],
                    },
                    "HEALTHCHECK_PORT": 443,
                    "HEALTHCHECK_ROUTE": f"/{ID}/geode/healthcheck",
                    "LISTENER_ARN": "arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f",
                    "ORIGINS": "https://next.geode-solutions.com",
                    "PING_ROUTE": f"/{ID}/geode/ping",
                    "SECONDS_BETWEEN_TRIES": 0.25,
                    "SECURITY_GROUP": "sg-0352ea112857ae7b9",
                    "SUBNET_ID": "subnet-0882d674b17515f6a",
                    "TASK_DEF_NAME": "TD_Website_Next",
                    "VPC_ID": "vpc-0e58c4d6976fb2aac",
                },
                "TEST": {
                    "API_URL": "https://api.geode-solutions.com",
                    "ASSIGN_PUBLIC_IP": "ENABLED",
                    "CLUSTER_NAME": "C_Website_Test",
                    "ENVIRONMENT_VARIABLES": {
                        "name": "geode",
                        "environment": [{"name": "ID", "value": ID}],
                    },
                    "HEALTHCHECK_PORT": 443,
                    "HEALTHCHECK_ROUTE": f"/{ID}/geode/healthcheck",
                    "LISTENER_ARN": "arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/ApiGeodeSolutions/4a4814e5912d42aa/70716e78eabafa1f",
                    "ORIGINS": "TO_COMPLETE",
                    "PING_ROUTE": f"/{ID}/geode/ping",
                    "SECONDS_BETWEEN_TRIES": 0.25,
                    "SECURITY_GROUP": "sg-0352ea112857ae7b9",
                    "SUBNET_ID": "subnet-0882d674b17515f6a",
                    "TASK_DEF_NAME": "TO_COMPLETE",
                    "VPC_ID": "vpc-0e58c4d6976fb2aac",
                },
            },
            "SHARETWIN": {
                "MASTER": {
                    "API_URL": "https://api.share-twin.com",
                    "ASSIGN_PUBLIC_IP": "ENABLED",
                    "CLUSTER_NAME": "C_ShareTwin_Master",
                    "ENVIRONMENT_VARIABLES": {
                        "name": "geode",
                        "environment": [{"name": "ID", "value": ID}],
                    },
                    "HEALTHCHECK_PORT": 443,
                    "HEALTHCHECK_ROUTE": f"/{ID}/geode/healthcheck",
                    "LISTENER_ARN": "arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4",
                    "PING_ROUTE": f"/{ID}/geode/ping",
                    "ORIGINS": "https://share-twin.com",
                    "SECONDS_BETWEEN_TRIES": 0.25,
                    "SECURITY_GROUP": "sg-01bcf5f64e3427fd3",
                    "SUBNET_ID": "subnet-0882d674b17515f6a",
                    "TASK_DEF_NAME": "TD_ShareTwin_Master",
                    "VPC_ID": "vpc-0e58c4d6976fb2aac",
                },
                "NEXT": {
                    "API_URL": "https://api.share-twin.com",
                    "ASSIGN_PUBLIC_IP": "ENABLED",
                    "CLUSTER_NAME": "C_ShareTwin_Next",
                    "ENVIRONMENT_VARIABLES": {
                        "name": "geode",
                        "environment": [{"name": "ID", "value": ID}],
                    },
                    "HEALTHCHECK_PORT": 443,
                    "HEALTHCHECK_ROUTE": f"/{ID}/geode/healthcheck",
                    "LISTENER_ARN": "arn:aws:elasticloadbalancing:eu-west-3:622060531233:listener/app/Api2GeodeSolutions/fd4af85f9ffc5a54/b559795c939115f4",
                    "PING_ROUTE": f"/{ID}/geode/ping",
                    "ORIGINS": "https://next.share-twin.com",
                    "SECONDS_BETWEEN_TRIES": 0.25,
                    "SECURITY_GROUP": "sg-07787694c5fdf2429",
                    "SUBNET_ID": "subnet-0882d674b17515f6a",
                    "TASK_DEF_NAME": "TD_ShareTwin_Next",
                    "VPC_ID": "vpc-0e58c4d6976fb2aac",
                },
            },
        }

        if "/website/" in REQUEST_PATH:
            CONFIG_TYPE = "WEBSITE"
            if REQUEST_ORIGIN == "":
                CONFIG_TYPE = "NEXT"
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]["MASTER"]["ORIGINS"]:
                CONFIG_ENV = "MASTER"
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]["NEXT"]["ORIGINS"]:
                CONFIG_ENV = "NEXT"
            elif "--geode-solutions.netlify.app" in REQUEST_ORIGIN:
                CONFIG_ENV = "TEST"
                task = REQUEST_ORIGIN[8:].split("--geode-solutions.netlify.app")[0]
                CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["ORIGINS"] = REQUEST_ORIGIN
                CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["TASK_DEF_NAME"] = task
        elif "/sharetwin/" in REQUEST_PATH:
            CONFIG_TYPE = "SHARETWIN"
            if REQUEST_ORIGIN == "":
                CONFIG_TYPE = "NEXT"
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]["MASTER"]["ORIGINS"]:
                CONFIG_ENV = "MASTER"
            elif REQUEST_ORIGIN == CONFIG_DICT[CONFIG_TYPE]["NEXT"]["ORIGINS"]:
                CONFIG_ENV = "NEXT"

        self.API_URL = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["API_URL"]
        self.ASSIGN_PUBLIC_IP = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["ASSIGN_PUBLIC_IP"]
        self.CLUSTER_NAME = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["CLUSTER_NAME"]
        self.ENVIRONMENT_VARIABLES = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV][
            "ENVIRONMENT_VARIABLES"
        ]
        self.HEALTHCHECK_PORT = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["HEALTHCHECK_PORT"]
        self.HEALTHCHECK_ROUTE = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV][
            "HEALTHCHECK_ROUTE"
        ]
        self.LISTENER_ARN = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["LISTENER_ARN"]
        self.PING_ROUTE = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["PING_ROUTE"]
        self.ORIGINS = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["ORIGINS"]
        self.SECONDS_BETWEEN_TRIES = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV][
            "SECONDS_BETWEEN_TRIES"
        ]
        self.SECURITY_GROUP = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["SECURITY_GROUP"]
        self.SUBNET_ID = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["SUBNET_ID"]
        self.TASK_DEF_NAME = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["TASK_DEF_NAME"]
        self.VPC_ID = CONFIG_DICT[CONFIG_TYPE][CONFIG_ENV]["VPC_ID"]


def make_lambda_return(
    CONFIG, STATUS_CODE: int, STATUS_DESCRIPTION: str, BODY: dict = None
):
    lamdba_return = dict(
        [
            ("statusCode", STATUS_CODE),
            ("statusDescription", STATUS_DESCRIPTION),
            ("isBase64Encoded", False),
            (
                "headers",
                dict(
                    [
                        ("Access-Control-Allow-Headers", "Content-Type"),
                        ("Access-Control-Allow-Origin", getattr(CONFIG, "ORIGINS")),
                        ("Access-Control-Allow-Methods", "OPTIONS,POST,GET"),
                        ("Content-Type", "application/json"),
                    ]
                ),
            ),
        ]
    )

    if BODY is not None:
        lamdba_return["body"] = json.dumps(BODY)
    return lamdba_return
