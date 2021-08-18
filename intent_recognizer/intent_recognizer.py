from kafka.consumer_kafka_wrapper import ConsumerKafkaWrapper
from kafka.producer_kafka_wrapper import ProducerKafkaWrapper
from utils.project_constants import to_IR_kafka_topic


class IntentRecognizer:
    def __init__(self):
        self.producer = ProducerKafkaWrapper()
        self.consumer = ConsumerKafkaWrapper()
        self.consumer.start_loop([to_IR_kafka_topic], self.process_message)

    @staticmethod
    def process_message(message):
        pass
