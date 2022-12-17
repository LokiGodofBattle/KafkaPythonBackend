from confluent_kafka import Producer
from confluent_kafka import Consumer
import socket
import threading
import logging
from flask import Flask, json

MIN_COMMIT_COUNT = 1

api = Flask(__name__)

event = threading.Event()

def basic_consume_loop(topics):
    running = True
    print("Service started", flush=True)

    conf = {'bootstrap.servers': "192.168.178.141:9092", 'group.id': "customer"}

    consumer = Consumer(conf)

    try:
        consumer.subscribe(topics)
        msg_count = 0

        while running:
            msg = consumer.poll()
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print("Data received", flush=True)
                if msg.key().decode("utf-8") == "data":
                    global data
                    data = msg.value().decode("utf-8")
                    print(data, flush=True)
                    print("event set", flush=True)
                    event.set()
        	
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

conf1 = {'bootstrap.servers': "192.168.178.141:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf1)

x = threading.Thread(target=basic_consume_loop, args=(["offerings_data"],))
x.start()

@api.route('/customer/getOfferings', methods=['GET'])
def get_offerings():
    producer.produce("offerings", key="cno", value="getOfferings")
    producer.flush()
    event.wait()
    print("event finished")
    event.clear()
    print(data)
    return data

api.run()

print("Message send")
