from lambdantic.apigateway.models import HttpMethod, Identity, RequestContext

from example.apigateway_simple_rest import handler

identity_mock = Identity(accountId='', apiKey='', caller='', sourceIp='', userAgent='')
request_context_mock = RequestContext(
    accountId='',
    apiId='',
    httpMethod=HttpMethod.GET,
    identity=identity_mock,
    requestId='',
    resourceId='',
    resourcePath='',
    stage='',
)


def test_pets_gets():
    assert handler(
        {
            'path': '/pets',
            'pathParameters': {},
            'resource': '',
            'requestContext': request_context_mock.dict(),
            'httpMethod': 'GET',
            'isBase64Encoded': False,
        },
        None,
    ) == {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'multiValueHeaders': {},
        'body': '[{"name": "dog", "age": 3, "pet_id": 1}, {"name": "cat", "age": 2, "pet_id": 2}]',
    }


def test_pets_get():
    assert handler(
        {
            'path': '/pets/1',
            'pathParameters': {},
            'resource': '',
            'requestContext': request_context_mock.dict(),
            'httpMethod': 'GET',
            'isBase64Encoded': False,
        },
        None,
    ) == {
        'body': '{"name": "dog", "age": 3, "pet_id": 1}',
        'headers': {},
        'isBase64Encoded': False,
        'multiValueHeaders': {},
        'statusCode': 200,
    }


def test_pets_get_invalid_id():
    assert handler(
        {
            'path': '/pets/abc',
            'pathParameters': {},
            'resource': '',
            'requestContext': request_context_mock.dict(),
            'httpMethod': 'GET',
            'isBase64Encoded': False,
        },
        None,
    ) == {
        'body': '',
        'headers': {},
        'isBase64Encoded': False,
        'multiValueHeaders': {},
        'statusCode': 400,
    }


def test_pets_post():
    assert handler(
        {
            'path': '/pets',
            'pathParameters': {},
            'resource': '',
            'requestContext': request_context_mock.dict(),
            'httpMethod': 'POST',
            'body': '{"name": "snake", "age": 1, "pet_id": 10}',
            'isBase64Encoded': False,
        },
        None,
    ) == {
        'body': '{"name": "snake", "age": 1, "pet_id": 2}',
        'headers': {},
        'isBase64Encoded': False,
        'multiValueHeaders': {},
        'statusCode': 201,
    }


def test_pets_post_invalid_body():
    assert handler(
        {
            'path': '/pets',
            'pathParameters': {},
            'resource': '',
            'requestContext': request_context_mock.dict(),
            'httpMethod': 'POST',
            'body': '{"name": "snake"}',
            'isBase64Encoded': False,
        },
        None,
    ) == {
        'body': '',
        'headers': {},
        'isBase64Encoded': False,
        'multiValueHeaders': {},
        'statusCode': 400,
    }
