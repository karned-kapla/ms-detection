import json
import logging
from confluent_kafka import Producer


class KafkaProducer:
    def __init__( self, config ):
        self.producer = Producer({'bootstrap.servers': config['bootstrap.servers']})
        logging.info(f"Producteur Kafka connecté à {config['bootstrap.servers']}")

    def send_message( self, topic, message ):
        try:
            logging.info(f"Sending message to topic {topic}")
            self.producer.produce(topic=topic, key='file', value=json.dumps(message))
            self.producer.flush()
            logging.info(f"Message envoyé au topic '{topic}'")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du message: {e}")
