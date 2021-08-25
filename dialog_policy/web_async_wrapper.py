import json

from aiohttp import web

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, UUID_TAG, \
    UUID_USERCHANNEL_TAG, UUID_USERID_TAG, ERROR_500_MESSAGE, PAYLOAD_INTENTS_TAG, INTENT_PROJECTS_TAG, \
    MESSAGE_TO_SKILL_MESSAGE_NAME, TO_SMART_APP
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
                UUID_TAG: {
                    UUID_USERCHANNEL_TAG: "FEBRUARY",
                    UUID_USERID_TAG: "1"
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

        if message_from_topic is None:
            return web.Response(text=ERROR_500_MESSAGE)

        IR_response_message_dict = json.loads(message_from_topic.value().decode('UTF-8'))

        intents = IR_response_message_dict.get(PAYLOAD_TAG, {}).get(PAYLOAD_INTENTS_TAG, {})
        for intent in intents.items():
            projects = intent[1].get(INTENT_PROJECTS_TAG, [])
            intent_name = intent[0]
            for project in projects:
                project_name = project.get("name")
                project_id = project.get("id")
                self._message_id += 1
                this_message_id = self._message_id
                app_request = json.dumps(
                    {
                        MESSAGE_NAME_TAG: MESSAGE_TO_SKILL_MESSAGE_NAME,
                        MESSAGE_ID_TAG: this_message_id,
                        UUID_TAG: {
                            UUID_USERCHANNEL_TAG: "OCTOBER",
                            "sub": "d2d6da62-6bdd-452b-b5dd-a145090075ba",
                            "userId": "123"
                        },
                        "payload": {
                            "app_info": {
                                "projectId": project_id
                            },
                            "intent": intent_name,
                            "projectName": project_name,
                            "message": {
                                "original_text": message
                            }
                        }
                    }
                )
                self.producer.produce(TO_SMART_APP, MESSAGE_TO_SKILL_MESSAGE_NAME, app_request)

        return web.Response(text=text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
