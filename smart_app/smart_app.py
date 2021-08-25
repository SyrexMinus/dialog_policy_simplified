import json

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_SMART_APP, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFY_TEXT_MESSAGE_NAME, \
    CLASSIFICATION_RESULT_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, \
    MESSAGE_TO_SKILL_MESSAGE_NAME, SMART_APP_RESPONSE_MESSAGE_NAME, UUID_TAG, UUID_USERCHANNEL_TAG, UUID_USERID_TAG, \
    SMART_APP_RESPONSE_KAFKA_TOPIC


class SmartApp:
    def __init__(self):
        self.producer = ProducerKafkaWrapper()
        self.consumer = ConsumerKafkaWrapper()
        self.consumer.start_loop([TO_SMART_APP], self.process_message)

    def process_message(self, message):
        message_string = message.value().decode('UTF-8')
        decoded_message = json.loads(message_string)
        this_message_id = decoded_message.get(MESSAGE_ID_TAG)

        # no message_id - no to whom to answer
        if this_message_id is None:
            return

        message_name = decoded_message.get(MESSAGE_NAME_TAG)

        if message_name == MESSAGE_TO_SKILL_MESSAGE_NAME:
            app_response = json.dumps(
                {
                    MESSAGE_ID_TAG: this_message_id,
                    UUID_TAG: {
                        UUID_USERCHANNEL_TAG: "app",
                        UUID_USERID_TAG: "123",
                        "sub": "test_sub"
                    },
                    "token": "0c4bd98a895beacb3ec8e9af868edeb9",
                    "sessionId": "test_session",
                    "sub": "12e",
                    MESSAGE_NAME_TAG: SMART_APP_RESPONSE_MESSAGE_NAME,
                    PAYLOAD_TAG: {}
                }
            )
            self.producer.produce(SMART_APP_RESPONSE_KAFKA_TOPIC, SMART_APP_RESPONSE_MESSAGE_NAME, app_response)
