import json

from aiohttp import web

from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import TO_IR_KAFKA_TOPIC, CLASSIFY_TEXT_MESSAGE_NAME, MESSAGE_ID_TAG, MESSAGE_NAME_TAG, \
    IR_RESPONSE_KAFKA_TOPIC, CLASSIFICATION_RESULT_MESSAGE_NAME, PAYLOAD_TAG, PAYLOAD_MESSAGE_TAG, UUID_TAG, \
    UUID_USERCHANNEL_TAG, UUID_USERID_TAG, ERROR_500_MESSAGE, PAYLOAD_INTENTS_TAG, INTENT_PROJECTS_TAG, \
    MESSAGE_TO_SKILL_MESSAGE_NAME, TO_SMART_APP_KAFKA_TOPIC, SMART_APP_RESPONSE_KAFKA_TOPIC, \
    APP_INFO_TAG, PROJECT_ID_TAG, PROJECT_NAME_TAG, ANSWER_TO_USER_MESSAGE_NAME, \
    BLENDER_REQUEST_MESSAGE_NAME, BLENDER_RESPONSE_MESSAGE_NAME, APP_RESPONSES_TAG
from utils.support_functions import IsOurKafkaResponceChecker, kafka_message_to_dict


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

        try:
            classified_message = self.classify_text_IR(message)

            classified_message_dict = kafka_message_to_dict(classified_message)
            intents = classified_message_dict.get(PAYLOAD_TAG, {}).get(PAYLOAD_INTENTS_TAG, {})

            apps_responses = self.apps_responses_on_message_to_skill(intents, message)

            blender_response_IR = self.blender_response_IR(apps_responses)

            blender_response_IR_dict = kafka_message_to_dict(blender_response_IR)

            response_dict = blender_response_IR_dict
            response_dict[MESSAGE_NAME_TAG] = ANSWER_TO_USER_MESSAGE_NAME
            response = str(response_dict)

            return web.Response(text=response)

        except ResponseException:
            print(ResponseException)
            return web.Response(text=ERROR_500_MESSAGE)

    def run_app(self):
        web.run_app(self.app)

    def _register_producer_kafka(self):
        self.producer = ProducerKafkaWrapper()

    def get_new_message_id(self):
        self._message_id += 1
        return self._message_id

    def classify_text_IR(self, message):
        this_message_id = self.get_new_message_id()
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
            raise ResponseException(CLASSIFICATION_RESULT_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC)

        return message_from_topic

    def apps_responses_on_message_to_skill(self, intents, message):
        sent_messages_ids = []
        for intent in intents.items():
            projects = intent[1].get(INTENT_PROJECTS_TAG, [])
            intent_name = intent[0]
            for project in projects:
                project_name = project.get("name")
                project_id = project.get("id")
                this_message_id = self.get_new_message_id()
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

        apps_responses = []
        messages_number = len(sent_messages_ids)
        for response_num in range(messages_number):
            is_our_response_checker = IsOurKafkaResponceChecker(message_ids=sent_messages_ids,
                                                                message_names=[ANSWER_TO_USER_MESSAGE_NAME])
            app_response = self.consumer.get_message(topics=[SMART_APP_RESPONSE_KAFKA_TOPIC],
                                                     return_expression=is_our_response_checker.check,
                                                     timeout=10)
            if app_response is None:
                raise ResponseException(ANSWER_TO_USER_MESSAGE_NAME, SMART_APP_RESPONSE_KAFKA_TOPIC)

            app_response_message_dict = kafka_message_to_dict(app_response)

            message_id = app_response_message_dict.get(MESSAGE_ID_TAG)
            apps_responses.append(app_response_message_dict)
            sent_messages_ids.remove(message_id)

        return apps_responses

    def blender_response_IR(self, apps_responses):
        this_message_id = self.get_new_message_id()
        IR_blender_request = json.dumps(
            {
                MESSAGE_NAME_TAG: BLENDER_REQUEST_MESSAGE_NAME,
                MESSAGE_ID_TAG: this_message_id,
                UUID_TAG: {
                    UUID_USERCHANNEL_TAG: "OCTOBER",
                    "sub": "d2d6da62-6bdd-452b-b5dd-a145090075ba",
                    "userId": "123"
                },
                PAYLOAD_TAG: {
                    APP_RESPONSES_TAG: str(apps_responses)
                }
            }
        )
        self.producer.produce(TO_IR_KAFKA_TOPIC, BLENDER_REQUEST_MESSAGE_NAME, IR_blender_request)

        is_our_IR_response_checker = IsOurKafkaResponceChecker(message_ids=[this_message_id],
                                                               message_names=[BLENDER_RESPONSE_MESSAGE_NAME])
        IR_blender_response = self.consumer.get_message(topics=[IR_RESPONSE_KAFKA_TOPIC],
                                                        return_expression=is_our_IR_response_checker.check,
                                                        timeout=10)

        if IR_blender_response is None:
            raise ResponseException(BLENDER_RESPONSE_MESSAGE_NAME, IR_RESPONSE_KAFKA_TOPIC)

        return IR_blender_response


class ResponseException(Exception):
    """Exception raised for errors in consuming kafka message.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message_name, topic_name, message="The response did not come"):
        self.message_name = message_name
        self.topic_name = topic_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'message {self.message_name}, topic {self.topic_name} -> {self.message}'
