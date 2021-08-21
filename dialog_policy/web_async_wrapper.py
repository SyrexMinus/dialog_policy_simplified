import json

from aiohttp import web

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME
from utils.support_functions import is_our_IR_response


class WebAsyncWrapper:
    def __init__(self):
        self.app = web.Application()
        self._configure_server()
        self._register_producer_kafka()
        self.consumer = ConsumerKafkaWrapper()

    def _configure_server(self):
        self._message_id = 1
        self.app.add_routes([web.get('/', self._handle),
                             web.get('/{message}', self._handle)])

    async def _handle(self, request):
        message = await request.match_info.get('message', "Anonymous")

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
                "payload": {
                    "message": message
                }
            }
        )

        await self.producer.produce(TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, classify_text_request)

        message_from_topic = self.consumer.start_loop([IR_RESPONSE_KAFKA_TOPIC],
                                                      is_our_IR_response(message, this_message_id),
                                                      loop=self.consumer.custom_consume_loop)

        text = f"I have got following kafka request: {message}. Request was sent to intent recognizer using kafka."

        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
