from confluent_kafka import Consumer
import threading
import logging

MIN_COMMIT_COUNT = 1

def basic_consume_loop(topics):
    print("Service started", flush=True)
    conf = {'bootstrap.servers': "192.168.178.141:9092", 'group.id': "observer"}

    consumer = Consumer(conf)

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
                print(msg.value().decode("utf-8"), flush=True)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

x = threading.Thread(target=basic_consume_loop, args=(["offerings", "offerings_data"],))
x.start()
