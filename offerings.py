import json
import threading
from confluent_kafka import Consumer

offerings = ["Bleistift", "Bleistift-Set", "Toaster"]

from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "192.168.178.141:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)

MIN_COMMIT_COUNT = 1

def basic_consume_loop(topics):
    print("Service started", flush=True)
    conf1 = {'bootstrap.servers': "192.168.178.141:9092", 'group.id': "offerings"}

    consumer = Consumer(conf1)

    running = True

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
                if msg.key().decode("utf-8") == "cno":
                    producer.produce("offerings_data", key="data", value=json.dumps(offerings))
                    producer.flush()
                    print("data send", flush=True)
                    msg_count += 1
                    if msg_count % MIN_COMMIT_COUNT == 0:
                        consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

x = threading.Thread(target=basic_consume_loop, args=(["offerings"],))
x.start()

