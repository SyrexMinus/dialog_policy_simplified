from config import kafka_bootstrap_servers

CONF_CONSUMER_KAFKA_DEFAULT = {'bootstrap.servers': kafka_bootstrap_servers,
                               'group.id': "default_consumer",
                               'auto.offset.reset': 'smallest'}

TO_IR_KAFKA_TOPIC = "to_IR"

IR_RESPONSE_KAFKA_TOPIC = "IR_responce"

CLASSIFY_TEXT_MESSAGE_NAME = "CLASSIFY_TEXT"

CLASSIFICATION_RESULT_MESSAGE_NAME = "CLASSIFICATION_RESULT"

MESSAGE_ID_TAG = "messageId"

MESSAGE_NAME_TAG = "messageName"
