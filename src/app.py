import time
import traceback


class WorkerApp:

    def __init__(self, kafka_client, message_processor, dlq_handler, signal_handler, logger):
        self.kafka_client = kafka_client
        self.message_processor = message_processor
        self.dlq_handler = dlq_handler
        self.signal_handler = signal_handler
        self.logger = logger

    def run(self):
        if not self.kafka_client.initialize():
            self.logger.failure("Échec de l'initialisation du client Kafka")
            return False

        if not self.kafka_client.connect_with_retries():
            self.logger.failure("Échec de la connexion à Kafka")
            return False

        self.logger.processing("Démarrage de la boucle principale de traitement des messages")

        heartbeat_counter = 0
        last_heartbeat_time = time.time()
        start_time = time.time()
        messages_processed = 0

        while self.signal_handler.is_running():
            try:
                msg = self.kafka_client.poll_message(1.0)

                current_time = int(time.time())
                if current_time - last_heartbeat_time >= 30:
                    heartbeat_counter += 1
                    uptime_minutes = int((current_time - start_time) / 60)
                    self.logger.heartbeat(
                        f"En attente de messages... (heartbeat #{heartbeat_counter}, {messages_processed} messages traités, uptime: {uptime_minutes} minutes)")
                    last_heartbeat_time = current_time

                if msg is None:
                    continue

                try:
                    self.message_processor.process(msg)
                    self.kafka_client.commit_message(msg)

                    messages_processed += 1
                    self.logger.check(f"Total des messages traités: {messages_processed}")
                except Exception as e:
                    self.dlq_handler.send_to_dlq(msg, e)

            except Exception as e:
                self.logger.exception(f"Erreur fatale: {e}")
                self.logger.traceback(traceback.format_exc())
                return False

        return True

    def shutdown(self):
        self.logger.disconnect("Fermeture...")
        self.kafka_client.close()
