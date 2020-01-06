from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MessageTypes(Enum):
    NOTIFICATION = 'Notification'
    UNSUBSCRIBE = 'UnsubscribeConfirmation'
    SUBSCRIBE = 'SubscriptionConfirmation'


class Notification(BaseModel):
    Type: MessageTypes = MessageTypes.NOTIFICATION
    MessageId: UUID
    Message: str
    Subject: Optional[str]
    Timestamp: datetime
    TopicArn: str
    SignatureVersion: str
    Signature: str
    SigningCertURL: str
    UnsubscribeURL: str


class SubscriptionConfirmation(BaseModel):
    Type: MessageTypes = MessageTypes.SUBSCRIBE
    MessageId: UUID
    Message: str
    Timestamp: datetime
    TopicArn: str
    SignatureVersion: str
    Signature: str
    SigningCertURL: str
    Token: str
    SubscribeURL: str


class UnsubscribeConfirmation(BaseModel):
    Type: MessageTypes = MessageTypes.UNSUBSCRIBE
    MessageId: UUID
    Message: str
    Timestamp: datetime
    TopicArn: str
    SignatureVersion: str
    Signature: str
    SigningCertURL: str
    Token: str
    SubscribeURL: str


class BackoffFunctions(Enum):
    LINEAR = 'linear'
    ARITHMETIC = 'arithmetic'
    GEOMETRIC = 'geometric'
    EXPONENTIAL = 'exponential'


class RetryPolicy(BaseModel):
    minDelayTarget: Optional[int]
    maxDelayTarget: Optional[int]
    numRetries: Optional[int]
    numMaxDelayRetries: Optional[int]
    backoffFunction: Optional[BackoffFunctions]


class ThrottlePolicy(BaseModel):
    maxReceivesPerSecond: Optional[int]


class SubscriptionAttributes(BaseModel):
    healthyRetryPolicy: RetryPolicy
    throttlePolicy: Optional[ThrottlePolicy]


class Http(BaseModel):
    defaultHealthyRetryPolicy: RetryPolicy
    defaultThrottlePolicy: Optional[ThrottlePolicy]
    disableSubscriptionOverrides: Optional[bool]


class TopicAttributes(BaseModel):
    http: Http
