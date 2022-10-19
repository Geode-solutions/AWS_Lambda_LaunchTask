def test_lambda_config():

    assert config.make_lambda_return(
        200, '200 OK', 'https://geode-solutions.com', {'ID': 123456}) is dict
