import logging
import sys
from config import LOG_LEVEL, MS_NAME


class Logger:
    EMOJIS = {
        'START': '🏗️',
        'INFO': 'ℹ️',
        'CHECK': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'DEBUG': '📊',
        'SAVE': '💾',
        'SEND': '📮',
        'RECEIVE': '📬',
        'MESSAGE': '✉️',
        'CONFIG': '⚙️',
        'INIT': '🔧',
        'RETRY': '🔄',
        'SUCCESS': '🎉',
        'FAILURE': '❗',
        'CONNECT': '🔗',
        'DISCONNECT': '🔌',
        'PROCESSING': '🔄',
        'RETRYING': '🔁',
        'WAITING': '⏳',
        'HEARTBEAT': '💓',
        'STOP': '🛑',
        'EXCEPTION': '🚨',
        'TRACEBACK': '🤬',
        'DATA': '📊',
        'API': '🌐',
        'DATABASE': '🗄️',
        'CACHE': '⚡',
        'SECURITY': '🔒',
        'USER': '👤',
        'TIME': '⏱️',
        'METRICS': '📈',
        'ALERT': '🔔',
        'SEARCH': '🔍',
        'FILTER': '🧹',
        'UPLOAD': '📤',
        'DOWNLOAD': '📥',
        'RUNNING': '🏃',
    }

    def __init__(self, app_name=MS_NAME):
        self.app_name = app_name
        log_level_name = LOG_LEVEL.upper()
        log_level = getattr(logging, log_level_name, logging.INFO)

        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        # Disable propagation to root logger to prevent duplicate logs
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, level, emoji_key, message):
        emoji = self.EMOJIS.get(emoji_key, '')
        log_message = f"{emoji} {message}"

        if level == 'info':
            self.logger.info(log_message)
        elif level == 'warning':
            self.logger.warning(log_message)
        elif level == 'error':
            self.logger.error(log_message)
        elif level == 'debug':
            self.logger.debug(log_message)

    def start(self, message):
        self.log('info', 'START', message)

    def info(self, message):
        self.log('info', 'INFO', message)

    def warning(self, message):
        self.log('warning', 'WARNING', message)

    def error(self, message):
        self.log('error', 'ERROR', message)

    def debug(self, message):
        self.log('debug', 'DEBUG', message)

    def heartbeat(self, message):
        self.log('info', 'HEARTBEAT', message)

    def stop(self, message):
        self.log('info', 'STOP', message)

    def config(self, message):
        self.log('info', 'CONFIG', message)

    def init(self, message):
        self.log('info', 'INIT', message)

    def retry(self, message):
        self.log('info', 'RETRY', message)

    def success(self, message):
        self.log('info', 'SUCCESS', message)

    def failure(self, message):
        self.log('error', 'FAILURE', message)

    def connect(self, message):
        self.log('info', 'CONNECT', message)

    def disconnect(self, message):
        self.log('info', 'DISCONNECT', message)

    def processing(self, message):
        self.log('info', 'PROCESSING', message)

    def check(self, message):
        self.log('info', 'CHECK', message)

    def retrying(self, message):
        self.log('info', 'RETRYING', message)

    def waiting(self, message):
        self.log('info', 'WAITING', message)

    def save(self, message):
        self.log('info', 'SAVE', message)

    def send(self, message):
        self.log('info', 'SEND', message)

    def receive(self, message):
        self.log('info', 'RECEIVE', message)

    def message(self, message):
        self.log('info', 'MESSAGE', message)

    def exception(self, message):
        self.log('error', 'EXCEPTION', message)

    def traceback(self, message):
        self.log('error', 'TRACEBACK', message)

    def data(self, message):
        self.log('info', 'DATA', message)

    def api(self, message):
        self.log('info', 'API', message)

    def database(self, message):
        self.log('info', 'DATABASE', message)

    def cache(self, message):
        self.log('info', 'CACHE', message)

    def security(self, message):
        self.log('info', 'SECURITY', message)

    def user(self, message):
        self.log('info', 'USER', message)

    def time(self, message):
        self.log('info', 'TIME', message)

    def metrics(self, message):
        self.log('info', 'METRICS', message)

    def alert(self, message):
        self.log('info', 'ALERT', message)

    def search(self, message):
        self.log('info', 'SEARCH', message)

    def filter(self, message):
        self.log('info', 'FILTER', message)

    def upload(self, message):
        self.log('info', 'UPLOAD', message)

    def download(self, message):
        self.log('info', 'DOWNLOAD', message)

    def running(self, message):
        self.log('info', 'RUNNING', message)
