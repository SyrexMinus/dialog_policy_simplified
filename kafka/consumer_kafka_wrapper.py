import sys
import time

from confluent_kafka import Consumer
from utils.project_constants import CONF_CONSUMER_KAFKA_DEFAULT
from confluent_kafka import KafkaError, KafkaException


class ConsumerKafkaWrapper:
    def __init__(self, conf=CONF_CONSUMER_KAFKA_DEFAULT):
        self.consumer = Consumer(conf)
        self.running = False

    def start_loop(self, topics, process_message_func, loop=None):
        self.running = True
        if loop:
            loop(topics, process_message_func)
        else:
            self._basic_consume_loop(topics, process_message_func)

    def shutdown(self):
        self.running = False

    def _basic_consume_loop(self, topics, process_message_func):
        try:
            self.consumer.subscribe(topics)

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    process_message_func(msg.value().decode('UTF-8'))
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def custom_consume_loop(self, topics, return_expression, timeout=1):
        try:
            self.consumer.subscribe(topics)

            start = time.time()
            while self.running:
                msg = self.consumer.poll(timeout=1)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    if return_expression(msg):
                        return msg

                if time.time() - start >= timeout:
                    return
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
