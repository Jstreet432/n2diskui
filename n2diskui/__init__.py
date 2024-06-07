import logging
import os
from flask import Flask
from config import config
from logging.handlers import RotatingFileHandler

def build_app(build_environment='development') -> Flask:

    app = Flask(__name__)
    app.config.from_object(config[build_environment])

    with app.app_context():
        from . import routes, api
    
    # This is for production and extra logging if we want to have it.
    # We can remove it later if we do not feel like using it.
    if not app.debug and not app.testing:
        # Set Logging Based on LOG_TO_STDOUT environment variable
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(app.config['LOG_LEVEL'])
            app.logger.addHandler(stream_handler)
        else:
            # If not outputting to stdout save in a file on user disk
            if not os.path.exists('n2diskui_logs'):
                os.mkdir('n2diskui_logs')
            file_stream_handler = RotatingFileHandler('n2diskui_logs/n2diskui.log', maxBytes=10240, backupCount=1)
            file_stream_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_stream_handler.setLevel(app.config['LOG_LEVEL'])
            app.logger.addHandler(file_stream_handler)
        
        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.info('App initialized successfully.')

    return app