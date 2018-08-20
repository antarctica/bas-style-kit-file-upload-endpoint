import logging

from flask import Flask
from raven.contrib.flask import Sentry
from flask_cors import CORS

from config import config
from file_upload_endpoint.main import main as main_blueprint

sentry = Sentry()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['APP_ENABLE_SENTRY']:
        sentry.init_app(app, logging=True, level=logging.WARNING)

    if app.config['APP_ENABLE_CORS']:
        CORS(
            app, 
            origins=app.config['CORS_ALLOWED_ORIGINS'], 
            methods=app.config['CORS_ALLOWED_METHODS'], 
            allow_headers=app.config['CORS_ALLOWED_HEADERS']
        )

    app.register_blueprint(main_blueprint)

    return app
