import sys
import traceback

from config import MS_NAME
from src.app import WorkerApp
from src.dlq_handler import DLQHandler
from src.kafka_client import KafkaClient
from src.logger_service import Logger
from src.message_processor import MessageProcessor
from src.signal_handler import SignalHandler

logger = Logger()


def main():
    logger.start(f"Starting {MS_NAME} Service")
    signal_handler = SignalHandler()
    kafka_client = KafkaClient(logger = logger)
    message_processor = MessageProcessor(logger = logger)
    dlq_handler = DLQHandler(producer = kafka_client.get_producer(), logger = logger)
    app = WorkerApp(
        kafka_client = kafka_client,
        message_processor = message_processor,
        dlq_handler = dlq_handler,
        signal_handler = signal_handler,
        logger = logger
    )

    try:
        success = app.run()
        if not success:
            logger.failure("Exception during launch")
            sys.exit(1)
    except Exception as e:
        logger.failure(f"Exception non gérée: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
