from unittest import TestCase

from lambdantic.sns.models import Notification

DATA = {
    "Type": "Notification",
    "MessageId": "22b80b92-fdea-4c2c-8f9d-bdfb0c7bf324",
    "TopicArn": "arn:aws:sns:us-west-2:123456789012:MyTopic",
    "Subject": "My First Message",
    "Message": "Hello world!",
    "Timestamp": "2012-05-02T00:54:06.655Z",
    "SignatureVersion": "1",
    "Signature": "EXAMPLEw6JRN...",
    "SigningCertURL": "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-f3ecfb7224c7233fe7bb5f59f96de52f.pem",
    "UnsubscribeURL": "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:123456789012:MyTopic:c9135db0-26c4-47ec-8998-413945fb5a96",
}


class TestNotification(TestCase):
    def test_validate(self):
        """ Correctly validates message """
        data = DATA.copy()
        Notification(**data)
