from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel

# Models created based on:
#   https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html


class Attributes(BaseModel):
    ApproximateReceiveCount: int
    SentTimestamp: int
    SequenceNumber: Optional[int]
    MessageGroupId: Optional[int]
    SenderId: str
    MessageDeduplicationId: Optional[int]
    ApproximateFirstReceiveTimestamp: int


class Record(BaseModel):
    messageId: UUID
    receiptHandle: str
    body: str
    attributes: Attributes
    messageAttributes: dict
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class Event(BaseModel):
    Records: List[Record]
