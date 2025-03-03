import signal
import logging


class SignalHandler:
    def __init__( self ):
        self.is_running = True
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop( self, sig, frame ):
        logging.info("Signal reçu, arrêt du consommateur...")
        self.is_running = False
