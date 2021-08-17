from aiohttp import web
from producer_kafka_wrapper import ProducerKafkaWrapper


class WebAsyncWrapper:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([web.get('/', self._handle),
                             web.get('/{kafka_request}', self._handle)])
        self._register_producer_kafka()

    async def _handle(self, request):
        kafka_request = request.match_info.get('kafka_request', "Anonymous")

        self.producer.produce("IR_requests", "message_to_recognize", kafka_request)

        text = f"I have got following kafka request: {kafka_request}. Request was sent to intent recognizer using kafka."
        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
