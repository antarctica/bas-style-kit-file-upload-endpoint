import sentry_sdk

from flask import Flask
from flask_cors import CORS

from config import config
from file_upload_endpoint.meta import meta as meta_blueprint
from file_upload_endpoint.main import main as main_blueprint
from file_upload_endpoint.meta.errors import error_handler_generic_bad_request, error_handler_generic_not_found, \
    error_handler_request_entity_too_large, error_handler_generic_internal_server_error
from file_upload_endpoint.middleware.request_id import RequestID


def create_app(config_name):
    app = Flask(__name__)

    # Config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Middleware / Wrappers
    if app.config['APP_ENABLE_SENTRY']:
        sentry_sdk.init(**app.config['SENTRY_CONFIG'])
    if app.config['APP_ENABLE_CORS']:
        CORS(app, **app.config['CORS_CONFIG'])
    RequestID(app)
    # Error handlers
    app.register_error_handler(400, error_handler_generic_bad_request)
    app.register_error_handler(404, error_handler_generic_not_found)
    app.register_error_handler(413, error_handler_request_entity_too_large)
    app.register_error_handler(500, error_handler_generic_internal_server_error)

    # App
    app.register_blueprint(meta_blueprint)
    app.register_blueprint(main_blueprint)

    return app
