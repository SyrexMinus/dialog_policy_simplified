import socket

producer_kafka_conf = {'bootstrap.servers': "localhost:9092",
                       'client.id': socket.gethostname()}
