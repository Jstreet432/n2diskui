import logging
import os

class Config:
    # Set environment variables here, these will become os.environ.gets
    SECRET_KEY = None
    SQL_DATABASE_URI = None
    # For now always log to stdout
    LOG_TO_STDOUT = True
    LOG_LEVEL = logging.INFO
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': Config

}