from flask import Flask
from .routes import bp
import logging

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp, url_prefix='/app')

    # Setup logging
    if not app.debug:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        logging.basicConfig(level=logging.DEBUG)

    app.logger.info("Flask application startup")
    
    return app