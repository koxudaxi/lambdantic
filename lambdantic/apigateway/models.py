from __future__ import annotations

import base64
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class HttpMethod(Enum):
    GET = 'GET'
    HEAD = 'HEAD'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTION = 'OPTION'
    PATCH = 'PATCH'


class Identity(BaseModel):
    cognitoIdentityPoolId: Optional[str]
    accountId: Optional[str]
    cognitoIdentityId: Optional[str]
    caller: Optional[str]
    apiKey: Optional[str]
    sourceIp: str
    cognitoAuthenticationType: Optional[str]
    cognitoAuthenticationProvider: Optional[str]
    userArn: Optional[str]
    userAgent: str
    user: Optional[str]


class RequestContext(BaseModel):
    accountId: str
    resourceId: str
    stage: str
    requestId: str
    identity: Identity
    resourcePath: str
    httpMethod: HttpMethod
    apiId: str


class Response(BaseModel):
    isBase64Encoded: bool = False  # true | false,
    statusCode: int = HTTPStatus.OK  # httpStatusCode,
    headers: Dict[str, str] = {}  # {"headerName": "headerValue", ...},
    multiValueHeaders: Dict[
        str, List[str]
    ] = {}  # {"headerName": ["headerValue", "headerValue2", ...], ...}
    body: str = ""  # "..."


class Request(BaseModel):
    resource: Optional[str]  # "Resource path"
    path: str  # "Path parameter",
    httpMethod: HttpMethod  # "Incoming request's method name"
    headers: Optional[Dict[str, str]]  # {String containing incoming request headers}
    multiValueHeaders: Optional[
        Dict[str, List[str]]
    ]  # {List of strings containing incoming request headers}
    queryStringParameters: Optional[Dict[str, str]]  # {query string parameters }
    multiValueQueryStringParameters: Optional[
        Dict[str, List[str]]
    ]  # {List of query string parameters}
    pathParameters: Dict[str, str]  # {path parameters}
    stageVariables: Optional[Dict[str, str]]  # {Applicable stage variables}
    requestContext: RequestContext  # {Request context, including authorizer-returned key-value pairs}
    body: Optional[str]  # "A JSON string of the request payload."
    isBase64Encoded: bool  # "A boolean flag to indicate if the applicable request payload is Base64-encode"
    decoded_body: Optional[str]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if self.isBase64Encoded:
            self.decoded_body = base64.b64decode(self.body).decode()  # type: ignore
        else:
            self.decoded_body = self.body
