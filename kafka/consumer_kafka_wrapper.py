import sys
import time

from confluent_kafka import Consumer
from utils.project_constants import CONF_CONSUMER_KAFKA_DEFAULT
from confluent_kafka import KafkaError, KafkaException


class ConsumerKafkaWrapper:
    def __init__(self, conf=CONF_CONSUMER_KAFKA_DEFAULT):
        self._consumer = Consumer(conf)
        self._running = False

    def start_loop(self, topics, process_message_func):
        self._running = True
        self._basic_consume_loop(topics=topics, process_message_func=process_message_func)

    def shutdown(self):
        self._running = False

    def _basic_consume_loop(self, topics, process_message_func):
        try:
            self._consumer.subscribe(topics)

            while self._running:
                msg = self._consumer.poll(timeout=1.0)
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
                    process_message_func(msg)
        finally:
            # Close down consumer to commit final offsets.
            self._consumer.close()

    def get_message(self, topics, return_expression, timeout=1):
        self._running = True
        return self._get_message_consume_loop(topics=topics, return_expression=return_expression, timeout=timeout)

    def _get_message_consume_loop(self, topics, return_expression, timeout):
        start = time.time()
        return_message = None

        try:
            self._consumer.subscribe(topics)

            while self._running:
                if time.time() - start >= timeout:
                    self.shutdown()

                msg = self._consumer.poll(timeout=1)
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
                        return_message = msg
                        self.shutdown()
        except:
            # Close down consumer to commit final offsets.
            self._consumer.close()
        finally:
            return return_message
