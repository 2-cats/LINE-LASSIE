from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

class Config:
    DB_HOST = app.config['DB_HOST']
    DB_USERNAME = app.config['DB_USERNAME']
    DB_PASSWORD = app.config['DB_PASSWORD']
    DB_NAME = app.config['DB_NAME']
    DB_PORT = app.config['DB_PORT']
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        Config.DB_USERNAME,
        Config.DB_PASSWORD,
        Config.DB_HOST,
        Config.DB_PORT,
        Config.DB_NAME
    )

class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        Config.DB_USERNAME,
        Config.DB_PASSWORD,
        Config.DB_HOST,
        Config.DB_PORT,
        Config.DB_NAME
    )

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        Config.DB_USERNAME,
        Config.DB_PASSWORD,
        Config.DB_HOST,
        Config.DB_PORT,
        Config.DB_NAME
    )

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
