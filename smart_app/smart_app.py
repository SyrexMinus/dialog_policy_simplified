import json

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_SMART_APP_KAFKA_TOPIC, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    CLASSIFY_TEXT_MESSAGE_NAME, \
    CLASSIFICATION_RESULT_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, \
    MESSAGE_TO_SKILL_MESSAGE_NAME, SMART_APP_RESPONSE_MESSAGE_NAME, UUID_TAG, UUID_USERCHANNEL_TAG, UUID_USERID_TAG, \
    SMART_APP_RESPONSE_KAFKA_TOPIC, ANSWER_TO_USER_MESSAGE_NAME, PROJECT_NAME_TAG, APP_INFO_TAG, PROJECT_ID_TAG


class SmartApp:
    def __init__(self):
        self.producer = ProducerKafkaWrapper()
        self.consumer = ConsumerKafkaWrapper()
        self.consumer.start_loop([TO_SMART_APP_KAFKA_TOPIC], self.process_message)

    def process_message(self, message):
        message_string = message.value().decode('UTF-8')
        decoded_message = json.loads(message_string)
        this_message_id = decoded_message.get(MESSAGE_ID_TAG)

        # no message_id - no to whom to answer
        if this_message_id is None:
            return

        message_name = decoded_message.get(MESSAGE_NAME_TAG)
        project_name = decoded_message.get(PAYLOAD_TAG, {}).get(PROJECT_NAME_TAG)
        project_id = decoded_message.get(PAYLOAD_TAG, {}).get(APP_INFO_TAG, {}).get(PROJECT_ID_TAG)

        if message_name == MESSAGE_TO_SKILL_MESSAGE_NAME:
            app_response = json.dumps(
                {
                    MESSAGE_ID_TAG: this_message_id,
                    MESSAGE_NAME_TAG: ANSWER_TO_USER_MESSAGE_NAME,
                    UUID_TAG: {
                        UUID_USERCHANNEL_TAG: "B2C",
                        UUID_USERID_TAG: "webdbg_userid_v3rd0bjqx4r5vkjw324g"
                    },
                    PAYLOAD_TAG: {
                        PROJECT_NAME_TAG: project_name,
                        APP_INFO_TAG: {
                            PROJECT_ID_TAG: project_id,
                        }
                    }
                }
            )
            self.producer.produce(SMART_APP_RESPONSE_KAFKA_TOPIC, SMART_APP_RESPONSE_MESSAGE_NAME, app_response)
