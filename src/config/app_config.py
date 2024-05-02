import logging

from typing import Literal
from logging.handlers import TimedRotatingFileHandler
from os import getenv, path
from pathlib import Path
from functools import lru_cache


class BaseConfig:
    # Common Configurations
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    BASE_DIR = Path(__file__).parent.parent
    SECRET_KEY = getenv("SECRET_KEY", "SomeSekrit!")
    TESTING = False
    CORS_ORIGINS = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:9999",
        "http://35.189.152.12",
        "http://35.194.118.131",
        "http://10.146.0.123",
        "http://10.146.0.124",
    ]


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    ENVIRONMENT = "production"
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    ENVIRONMENT = "testing"
    TESTING = True


configurations = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


@lru_cache()
def get_settings() -> BaseConfig:
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = getenv("ENVIRONMENT", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
