from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageTypes(Enum):
    NOTIFICATION = 'Notification'
    UNSUBSCRIBE = 'UnsubscribeConfirmation'
    SUBSCRIBE = 'SubscriptionConfirmation'


class Base(BaseModel):
    Type: MessageTypes
    MessageId: UUID
    TopicArn: str
    Timestamp: datetime
    SignatureVersion: str
    Signature: str
    SigningCertURL: str


class Notification(Base):
    Type: MessageTypes = MessageTypes.NOTIFICATION
    Subject: Optional[str]
    Message: str
    UnsubscribeURL: str


class Confirmation(Base):
    Token: MessageTypes
    Message: str
    SubscribeURL: str


class SubscriptionConfirmation(Confirmation):
    Type: MessageTypes = MessageTypes.SUBSCRIBE


class UnsubscribeConfirmation(Confirmation):
    Type: MessageTypes = MessageTypes.UNSUBSCRIBE
