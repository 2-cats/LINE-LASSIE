from flask import Flask
import os
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_PORT'],
        app.config['DB_NAME']
    )
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_USERNAME = app.config['MQTT_USERNAME']
    MQTT_PASSWORD = app.config['MQTT_PASSWORD']

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    pjdir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(pjdir, 'test.db')
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_USERNAME = app.config['MQTT_USERNAME']
    MQTT_PASSWORD = app.config['MQTT_PASSWORD']

class ProductionConfig(Config):
    pjdir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_PORT'],
        app.config['DB_NAME']
    )
    MQTT_TLS_ENABLED = True
    MQTT_TLS_VERSION = 2
    MQTT_CLIENT_ID = app.config['MQTT_CLIENT_ID']
    MQTT_BROKER_URL = app.config['MQTT_HOSTNAME']
    MQTT_BROKER_PORT = app.config['MQTT_PORT']
    MQTT_TLS_CA_CERTS = os.path.join(pjdir, app.config['MQTT_CA_CERTS'])
    MQTT_TLS_CERTFILE = os.path.join(pjdir, app.config['MQTT_CERTFILE'])
    MQTT_TLS_KEYFILE = os.path.join(pjdir, app.config['MQTT_KEYFILE'])

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
