import os
import logging
from logging import StreamHandler
from dotenv import load_dotenv


class Config(object):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DEBUG = False
    TESTING = False
    APP_ENABLE_SENTRY = os.environ.get('APP_ENABLE_SENTRY') or True
    APP_ENABLE_CORS = os.environ.get('APP_ENABLE_CORS') or True

    MAX_CONTENT_LENGTH = os.environ.get('APP_MAX_UPLOAD_BYTES') or 10 * 1024 * 1024  # 10MB

    SENTRY_CONFIG = {}
    SENTRY_CONFIG['environment'] = os.getenv('FLASK_ENV')
    if 'APP_RELEASE' in os.environ:
        SENTRY_CONFIG['release'] = os.environ.get('APP_RELEASE')

    CORS_ALLOWED_ORIGINS = [
        'http://localhost:9000', 
        'https://style-kit-testbed.web.bas.ac.uk', 
        'https://style-kit-testing.web.bas.ac.uk', 
        'https://style-kit.web.bas.ac.uk'
    ]
    CORS_ALLOWED_METHODS = [
        'OPTIONS',
        'GET',
        'POST'
    ]
    CORS_ALLOWED_HEADERS = [
        'cache-control',
        'x-requested-with'
    ]

    @staticmethod
    def init_app(app):
        # Log to stderr
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    APP_ENABLE_SENTRY = os.environ.get('APP_ENABLE_SENTRY') or False

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    APP_ENABLE_SENTRY = os.environ.get('APP_ENABLE_SENTRY') or False

class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': ProductionConfig
}
