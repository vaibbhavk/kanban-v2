import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://default:redispw@localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://default:redispw@localhost:6379/2"
    REDIS_URL = "redis://default:redispw@localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(SQLITE_DB_DIR, "kanban_db.sqlite3")
    DEBUG = True
    JWT_SECRET_KEY = "thisisasecret"
    JWT_ACCESS_TOKEN_EXPIRES = 50000000000
    CELERY_BROKER_URL = "redis://default:redispw@localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://default:redispw@localhost:6379/2"
    REDIS_URL = "redis://default:redispw@localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 50
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "vaibhav@email.com"
    SENDER_PASSWORD = ""
