import json

from utils.project_constants import MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFICATION_RESULT_MESSAGE_NAME


class IsOurIRResponceChecker:
    def __init__(self, message_id, message_name):
        self.message_id = message_id
        self.message_name = message_name

    def check(self, message):
        try:
            message_string = message.value().decode('UTF-8')
            decoded_message = json.loads(message_string)
            return decoded_message[MESSAGE_ID_TAG] == self.message_id and \
                   decoded_message[MESSAGE_NAME_TAG] == self.message_name
        finally:
            pass
        return False
