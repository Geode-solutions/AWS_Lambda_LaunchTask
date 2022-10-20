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
