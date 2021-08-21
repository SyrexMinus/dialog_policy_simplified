import json

from utils.project_constants import MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFICATION_RESULT_MESSAGE_NAME


def is_our_IR_response(message, message_id):
    try:
        decoded_message = json.loads(message)
        return decoded_message[MESSAGE_ID_TAG] == message_id and \
               decoded_message[MESSAGE_NAME_TAG] == CLASSIFICATION_RESULT_MESSAGE_NAME
    finally:
        return False
