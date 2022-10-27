import json


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
