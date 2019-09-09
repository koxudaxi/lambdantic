from __future__ import annotations

from typing import Optional

from .models import Response


class LambdaError(Exception):
    def __init__(self, response: Response, error: Optional[Exception] = None):
        self.response: Response = response
        self.error: Optional[Exception] = error
