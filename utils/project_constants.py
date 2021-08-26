from config import kafka_bootstrap_servers

CONF_CONSUMER_KAFKA_DEFAULT = {'bootstrap.servers': kafka_bootstrap_servers,
                               'group.id': "default_consumer",
                               'auto.offset.reset': 'smallest'}

TO_IR_KAFKA_TOPIC = "to_IR"

TO_SMART_APP_KAFKA_TOPIC = "to_smart_app"

IR_RESPONSE_KAFKA_TOPIC = "IR_response"

SMART_APP_RESPONSE_KAFKA_TOPIC = "smart_app_response"

CLASSIFY_TEXT_MESSAGE_NAME = "CLASSIFY_TEXT"

CLASSIFICATION_RESULT_MESSAGE_NAME = "CLASSIFICATION_RESULT"

MESSAGE_TO_SKILL_MESSAGE_NAME = "MESSAGE_TO_SKILL"

SMART_APP_RESPONSE_MESSAGE_NAME = "SERVER_ACTION"

ANSWER_TO_USER_MESSAGE_NAME = "ANSWER_TO_USER"

MESSAGE_ID_TAG = "messageId"

PAYLOAD_INTENTS_TAG = "intents"

INTENT_PROJECTS_TAG = "projects"

MESSAGE_NAME_TAG = "messageName"

PAYLOAD_TAG = "payload"

PAYLOAD_MESSAGE_TAG = "message"

UUID_TAG = "uuid"

UUID_USERCHANNEL_TAG = "userChannel"

UUID_USERID_TAG = "userId"

PROJECT_NAME_TAG = "projectName"

PROJECT_ID_TAG = "projectId"

APP_INFO_TAG = "app_info"

ERROR_500_MESSAGE = "500 Internal Server Error"
