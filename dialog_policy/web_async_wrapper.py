import json

from aiohttp import web

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, UUID_TAG, \
    UUID_USERCHANNEL_TAG, UUID_USERID_TAG, ERROR_500_MESSAGE, PAYLOAD_INTENTS_TAG, INTENT_PROJECTS_TAG, \
    MESSAGE_TO_SKILL_MESSAGE_NAME, TO_SMART_APP_KAFKA_TOPIC, SMART_APP_RESPONSE_KAFKA_TOPIC, \
    SMART_APP_RESPONSE_MESSAGE_NAME, APP_INFO_TAG, PROJECT_ID_TAG, PROJECT_NAME_TAG, ANSWER_TO_USER_MESSAGE_NAME
from utils.support_functions import IsOurKafkaResponceChecker


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

        is_our_IR_response_checker = IsOurKafkaResponceChecker(message_ids=[this_message_id],
                                                               message_names=[CLASSIFICATION_RESULT_MESSAGE_NAME])
        message_from_topic = self.consumer.get_message(topics=[IR_RESPONSE_KAFKA_TOPIC],
                                                       return_expression=is_our_IR_response_checker.check,
                                                       timeout=10)

        if message_from_topic is None:
            return web.Response(text=ERROR_500_MESSAGE)

        IR_response_message_dict = json.loads(message_from_topic.value().decode('UTF-8'))

        intents = IR_response_message_dict.get(PAYLOAD_TAG, {}).get(PAYLOAD_INTENTS_TAG, {})
        sent_messages_ids = []
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
                        PAYLOAD_TAG: {
                            APP_INFO_TAG: {
                                PROJECT_ID_TAG: project_id
                            },
                            "intent": intent_name,
                            PROJECT_NAME_TAG: project_name,
                            "message": {
                                "original_text": message
                            }
                        }
                    }
                )
                self.producer.produce(TO_SMART_APP_KAFKA_TOPIC, MESSAGE_TO_SKILL_MESSAGE_NAME, app_request)
                sent_messages_ids.append(this_message_id)

        debug_text = ""
        app_responses = []
        for response_num in range(len(sent_messages_ids)):
            is_our_response_checker = IsOurKafkaResponceChecker(message_ids=sent_messages_ids,
                                                                message_names=[ANSWER_TO_USER_MESSAGE_NAME])
            app_response = self.consumer.get_message(topics=[SMART_APP_RESPONSE_KAFKA_TOPIC],
                                                     return_expression=is_our_response_checker.check,
                                                     timeout=10)
            if app_response:
                app_response_message_dict = json.loads(app_response.value().decode('UTF-8'))

                message_id = app_response_message_dict.get(MESSAGE_ID_TAG)
                app_responses.append(app_response)
                sent_messages_ids.remove(message_id)
                debug_text += app_response.value().decode('UTF-8')

        return web.Response(text=debug_text)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()
