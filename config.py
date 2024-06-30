import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    FLASK_CONFIG = "DEV"
    TESTING = True
    DEBUG = True


class TestingConfig(Config):
    FLASK_CONFIG = "TEST"
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    FLASK_CONFIG = "STAGING"
    TESTING = False
    DEBUG = False


class ProductionConfig(Config):
    FLASK_CONFIG = "PROD"
    TESTING = False
    DEBUG = False


config = {
    "DEV": DevelopmentConfig,
    "TEST": TestingConfig,
    "STAGING": StagingConfig,
    "PROD": ProductionConfig,
}
