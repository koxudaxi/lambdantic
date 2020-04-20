from datetime import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel

# Models created based on:
#   https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html


class RequestParameters(BaseModel):
    sourceIPAddress: str


class Identity(BaseModel):
    principalId: str


class Bucket(BaseModel):
    name: str
    ownerIdentity: Identity
    arn: str


class Object(BaseModel):
    key: str
    size: int
    eTag: str
    sequencer: str


class S3(BaseModel):
    s3SchemaVersion: str
    configurationId: UUID
    bucket: Bucket
    object: Object


class Record(BaseModel):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: datetime
    eventName: str
    userIdentity: Identity
    requestParameters: RequestParameters
    responseElements: Dict[str, str]
    s3: S3


class Event(BaseModel):
    Records: List[Record]
