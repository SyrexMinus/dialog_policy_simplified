import json

from aiohttp import web
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG


class WebAsyncWrapper:
    def __init__(self):
        self.app = web.Application()
        self._configure_server()
        self._register_producer_kafka()

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

        text = f"I have got following kafka request: {message}. Request was sent to intent recognizer using kafka."

        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
