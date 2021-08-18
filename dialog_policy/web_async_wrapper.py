import json

from aiohttp import web
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import to_IR_kafka_topic


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
                "messageId": this_message_id,
                "messageName": "CLASSIFY_TEXT",
                "payload": {
                    "message": message
                }
            }
        )

        self.producer.produce(to_IR_kafka_topic, "CLASSIFY_TEXT", classify_text_request)

        text = f"I have got following kafka request: {classify_text_request}. Request was sent to intent recognizer using kafka."

        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
