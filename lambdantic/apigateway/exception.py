from typing import Optional

from lambdantic.apigateway import Response


class LambdaError(Exception):
    def __init__(self, response: Response, error: Optional[Exception] = None):
        self.response: Response = response
        self.error: Optional[Exception] = error
