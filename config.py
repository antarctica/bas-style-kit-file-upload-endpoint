import os
import logging
from logging import StreamHandler
from dotenv import load_dotenv

class Config(object):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DEBUG = False
    APP_ENDPOINT_BASE = os.environ.get('APP_ENDPOINT_BASE')
    MAX_CONTENT_LENGTH = os.environ.get('APP_MAX_UPLOAD_BYTES') or 10 * 1024 * 1024  # 10MB

    def init_app(self, app):
        # Log to stderr
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    APP_ENDPOINT_BASE = os.environ.get('APP_ENDPOINT_BASE') or 'http://localhost:9000'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
