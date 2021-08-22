import json

from aiohttp import web

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG
from utils.support_functions import IsOurIRResponceChecker


class WebAsyncWrapper:
    def __init__(self):
        self.app = web.Application()
        self._configure_server()
        self._register_producer_kafka()
        self.consumer = ConsumerKafkaWrapper()

    def _configure_server(self):
        self._message_id = 0
        self.app.add_routes([web.get('/', self._handle),
                             web.get('/{message}', self._handle)])

    async def _handle(self, request):
        message = request.match_info.get('message', "Anonymous")

        self._message_id += 1
        this_message_id = self._message_id

        classify_text_request = json.dumps(
            {
                MESSAGE_ID_TAG: this_message_id,
                MESSAGE_NAME_TAG: CLASSIFY_TEXT_MESSAGE_NAME,
                "uuid": {
                    "userChannel": "FEBRUARY",
                    "userId": "1"
                },
                PAYLOAD_TAG: {
                    PAYLOAD_MESSAGE_TAG: message
                }
            }
        )

        self.producer.produce(TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, classify_text_request)

        is_our_IR_response_checker = IsOurIRResponceChecker(this_message_id, CLASSIFICATION_RESULT_MESSAGE_NAME)

        message_from_topic = self.consumer.get_message(topics=[IR_RESPONSE_KAFKA_TOPIC],
                                                       return_expression=is_our_IR_response_checker.check,
                                                       timeout=10)

        message_text = "500 Internal Server Error"
        if message_from_topic:
            message_text = message_from_topic.value().decode('UTF-8')

        text = f"IR decoded this as \"{message_text}\""

        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
