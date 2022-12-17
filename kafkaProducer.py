from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "192.168.178.141:49155",
        'client.id': socket.gethostname()}

producer = Producer(conf)

producer.produce("offerings", key="cno", value="getOfferings")
producer.flush()
