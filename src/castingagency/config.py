import os

class BaseConfig:
    APP = 'castingagency'
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'jamaal'


class DevelopmentConfig(BaseConfig):
    # ENV = 'development'
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    # ENV = 'development'
    TESTING = True
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    # ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
