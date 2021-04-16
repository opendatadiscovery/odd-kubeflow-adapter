import os
from typing import Any

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s [%(processName)s]: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}


class MissingEnvironmentVariable(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def get_env(env: str, default_value: Any = None) -> Any:
    try:
        return os.environ.get(env)
    except KeyError:
        if default_value is not None:
            return default_value
        raise MissingEnvironmentVariable(f"{env} does not exist")


class BaseConfig:
    KUBEFLOW_HOST = get_env("KUBEFLOW_HOST")
    KUBEFLOW_NAMESPACE = get_env("KUBEFLOW_NAMESPACE")
    KUBEFLOW_SESSION_COOKIE0 = get_env("KUBEFLOW_SESSION_COOKIE0") or None
    KUBEFLOW_SESSION_COOKIE1 = get_env("KUBEFLOW_SESSION_COOKIE1") or None


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = False
