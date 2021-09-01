import json
from collections import Collection

from utils.project_constants import MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFICATION_RESULT_MESSAGE_NAME


class IsOurKafkaResponceChecker:
    def __init__(self, message_ids: Collection, message_names: Collection):
        self.message_ids = message_ids
        self.message_names = message_names

    def check(self, message):
        try:
            message_string = message.value().decode('UTF-8')
            decoded_message = json.loads(message_string)
            return decoded_message[MESSAGE_ID_TAG] in self.message_ids and \
                   decoded_message[MESSAGE_NAME_TAG] in self.message_names
        finally:
            pass
        return False


def kafka_message_to_dict(kafka_message):
    return json.loads(kafka_message.value().decode('UTF-8'))


class ResponseException(Exception):
    """Exception raised for errors in consuming kafka message.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message_name, topic_name, message="The response did not come"):
        self.message_name = message_name
        self.topic_name = topic_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'message {self.message_name}, topic {self.topic_name} -> {self.message}'
