import os
import logging
from logging import StreamHandler
# noinspection PyPackageRequirements
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration
from str2bool import str2bool


class Config(object):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DEBUG = False
    TESTING = False
    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or True
    APP_ENABLE_CORS = str2bool(os.environ.get('APP_ENABLE_CORS')) or True

    MAX_CONTENT_LENGTH = int(os.environ.get('APP_MAX_UPLOAD_BYTES', 10 * 1024 * 1024))  # default: 10MB

    SENTRY_CONFIG = {
        'integrations': [FlaskIntegration()],
        'environment': os.getenv('FLASK_ENV') or 'default'
    }
    if 'APP_RELEASE' in os.environ:
        SENTRY_CONFIG['release'] = os.environ.get('APP_RELEASE')

    CORS_CONFIG = {
        'origins': [
            'http://localhost:9000',
            'https://style-kit-testbed.web.bas.ac.uk',
            'https://style-kit-testing.web.bas.ac.uk',
            'https://style-kit.web.bas.ac.uk'
        ],
        'methods': [
            'OPTIONS',
            'GET',
            'POST'
        ],
        'allowed_headers': [
            'cache-control',
            'x-requested-with'
        ]
    }

    @staticmethod
    def init_app(app):
        # Log to stderr
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or False

class TestConfig(Config):
    ENV = 'testing'

    DEBUG = True
    TESTING = True
    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or False


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': ProductionConfig
}
