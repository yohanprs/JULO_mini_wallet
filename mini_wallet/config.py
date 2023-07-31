import os
from logging.config import dictConfig

from mini_wallet.env import EnvConfig

env = EnvConfig("MINIWALLET")
here = os.path.abspath(os.path.dirname(__file__))


class Config:
    _basedir = os.path.abspath(os.path.dirname(__file__))    

    FLASK_DEBUG = env.boolean("DEBUG", False)

    # Database Config
    DB_NAME = env.string("DB_NAME", "akuser")
    DB_USER = env.string("DB_USER", "akuser")
    DB_PASS = env.string("DB_PASS", "password")
    DB_HOST = env.string("DB_HOST", "localhost")
    DB_PORT = env.string("DB_PORT", "5432")

    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://" f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = env.int("SQLALCHEMY_POOL_TIMEOUT", 60)
    SQLALCHEMY_POOL_SIZE = env.int("SQLALCHEMY_POOL_SIZE", 50)
    SQLALCHEMY_POOL_RECYCLE = env.int("SQLALCHEMY_POOL_SIZE", 120)
    SQLALCHEMY_MAX_OVERFLOW = env.int("SQLALCHEMY_MAX_OVERFLOW", 50)

    # App Configuration
    DATETIME_FORMAT = env.string("DATETIME_FORMAT", "%A, %d %B %Y %H:%M:%S")