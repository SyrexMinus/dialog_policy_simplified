import json

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, CLASSIFY_TEXT_MESSAGE_NAME, \
    CLASSIFICATION_RESULT_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC


class IntentRecognizer:
    def __init__(self):
        self.producer = ProducerKafkaWrapper()
        self.consumer = ConsumerKafkaWrapper()
        self.consumer.start_loop([TO_IR_KAFKA_TOPIC], self.process_message)

    def process_message(self, message):
        decoded_message = json.loads(message)
        this_message_id = decoded_message.get(MESSAGE_ID_TAG)

        # no message_id - no to whom to answer
        if this_message_id is None:
            return

        message_name = decoded_message.get(MESSAGE_NAME_TAG)

        if message_name == CLASSIFY_TEXT_MESSAGE_NAME:
            classify_text_request = json.dumps(
                {
                    MESSAGE_ID_TAG: this_message_id,
                    MESSAGE_NAME_TAG: CLASSIFICATION_RESULT_MESSAGE_NAME,
                    "uuid": {
                        "userChannel": "FEBRUARY",
                        "userId": "1"
                    },
                    "payload": {
                        "intents": {
                            "weather": {
                                "score": 1.0,
                                "interrupt_exclusive_app": False,
                                "meta": {},
                                "projects": [
                                    {"name": "weatherApp", "id": "9a662582-140d-4e8a-a3bb-cf786d5cfe1f"}
                                ]
                            }
                        },
                        "message": {
                            "original_text": "message"
                        }
                    }
                }
            )
            await self.producer.produce(IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME,
                                        classify_text_request)
