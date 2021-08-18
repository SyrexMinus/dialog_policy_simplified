from confluent_kafka import Producer
from config import conf_producer_kafka


class ProducerKafkaWrapper:

    def __init__(self):
        self.producer = Producer(conf_producer_kafka)

    def produce(self, topic, key, value):
        self.producer.produce(topic=topic, key=key, value=value, callback=self._acked)

        # Wait up to 1 second for events. Callbacks will be invoked during
        # this method call if the message is acknowledged.
        self.producer.poll(1)

    @staticmethod
    def _acked(err, msg):
        if err is not None:
            print(f"Failed to deliver message: {msg.topic().decode('UTF-8')} {msg.key().decode('UTF-8')} {msg.value().decode('UTF-8')}: {str(err)}")
        else:
            print(f"Message produced: {msg.topic()} {msg.key().decode('UTF-8')} {msg.value().decode('UTF-8')}")
