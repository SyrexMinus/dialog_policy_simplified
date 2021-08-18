from config import kafka_bootstrap_servers

conf_consumer_kafka_default = {'bootstrap.servers': kafka_bootstrap_servers,
                               'group.id': "default_consumer",
                               'auto.offset.reset': 'smallest'}

to_IR_kafka_topic = "to_IR"
