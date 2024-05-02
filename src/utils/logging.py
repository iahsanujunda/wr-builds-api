import logging
import logging.config
import os


def configure_logging():
    logging_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s: %(levelname)s] [%(pathname)s:%(lineno)d] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO" if os.getenv("ENVIRONMENT") == "production" else "DEBUG",
        },
        "loggers": {
            "project": {
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_dict)
