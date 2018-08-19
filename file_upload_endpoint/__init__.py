import logging

from flask import Flask
from raven.contrib.flask import Sentry

from config import config
from file_upload_endpoint.main import main as main_blueprint

sentry = Sentry()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['APP_ENABLE_SENTRY']:
        sentry.init_app(app, logging=True, level=logging.WARNING)

    app.register_blueprint(main_blueprint)

    return app
