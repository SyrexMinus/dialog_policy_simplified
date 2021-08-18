import socket

kafka_bootstrap_servers = "localhost:9092"

conf_producer_kafka = {"bootstrap.servers": kafka_bootstrap_servers,
                       "client.id": socket.gethostname()}
