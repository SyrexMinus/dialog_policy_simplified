import json

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFY_TEXT_MESSAGE_NAME, \
    CLASSIFICATION_RESULT_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, UUID_TAG, \
    UUID_USERCHANNEL_TAG, UUID_USERID_TAG, PAYLOAD_INTENTS_TAG, INTENT_PROJECTS_TAG, BLENDER_REQUEST_MESSAGE_NAME, \
    BLENDER_RESPONSE_MESSAGE_NAME, APP_RESPONSES_TAG


class IntentRecognizer:
    def __init__(self):
        self.producer = ProducerKafkaWrapper()
        self.consumer = ConsumerKafkaWrapper()
        self.consumer.start_loop([TO_IR_KAFKA_TOPIC], self.process_message)

    def process_message(self, message):
        message_string = message.value().decode('UTF-8')
        decoded_message = json.loads(message_string)
        this_message_id = decoded_message.get(MESSAGE_ID_TAG)

        # no message_id - no to whom to answer
        if this_message_id is None:
            return

        message_name = decoded_message.get(MESSAGE_NAME_TAG)
        message_text = decoded_message.get(PAYLOAD_TAG, {}).get(PAYLOAD_MESSAGE_TAG)
        uuid_user_channel = decoded_message.get(UUID_TAG, {}).get(UUID_USERCHANNEL_TAG)
        uuid_user_id = decoded_message.get(UUID_TAG, {}).get(UUID_USERID_TAG)
        app_responses = decoded_message.get(PAYLOAD_TAG, {}).get(APP_RESPONSES_TAG)

        if message_name == CLASSIFY_TEXT_MESSAGE_NAME:
            classification_result_response = json.dumps(
                {
                    MESSAGE_ID_TAG: this_message_id,
                    MESSAGE_NAME_TAG: CLASSIFICATION_RESULT_MESSAGE_NAME,
                    UUID_TAG: {
                        UUID_USERCHANNEL_TAG: uuid_user_channel,
                        UUID_USERID_TAG: uuid_user_id
                    },
                    PAYLOAD_TAG: {
                        PAYLOAD_INTENTS_TAG: {
                            "weather": {
                                "score": 1.0,
                                "interrupt_exclusive_app": False,
                                "meta": {},
                                INTENT_PROJECTS_TAG: [
                                    {"name": "weatherApp", "id": "9a662582-140d-4e8a-a3bb-cf786d5cfe1f"}
                                ]
                            }
                        },
                        PAYLOAD_MESSAGE_TAG: {
                            "original_text": message_text
                        }
                    }
                }
            )
            self.producer.produce(IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME,
                                  classification_result_response)

        if message_name == BLENDER_REQUEST_MESSAGE_NAME:
            blender_result_response = json.dumps(
                {
                    MESSAGE_ID_TAG: this_message_id,
                    MESSAGE_NAME_TAG: BLENDER_RESPONSE_MESSAGE_NAME,
                    UUID_TAG: {
                        UUID_USERCHANNEL_TAG: uuid_user_channel,
                        UUID_USERID_TAG: uuid_user_id
                    },
                    PAYLOAD_TAG: {
                        APP_RESPONSES_TAG: app_responses
                    }
                }
            )
            self.producer.produce(IR_RESPONSE_KAFKA_TOPIC, BLENDER_RESPONSE_MESSAGE_NAME,
                                  blender_result_response)
