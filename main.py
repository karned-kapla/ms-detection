import json
from confluent_kafka import Consumer, KafkaError

consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['new'])

print("En attente de messages...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Erreur Kafka: {msg.error()}")
                break

        data = json.loads(msg.value().decode('utf-8'))
        print(f"Reçu: {data}")

except KeyboardInterrupt:
    print("Arrêt du consommateur...")
finally:
    consumer.close()
