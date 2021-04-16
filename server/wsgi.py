import os
from logging.config import dictConfig
from odd_contract import init_flask_app, init_controller
from controllers import OpenDataDiscoveryController
from adapter import KubeflowAdapter
from flask import Response

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
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
)


def create_app(conf):
    app = init_flask_app()
    app.config.from_object(conf)
    app.add_url_rule('/health', "healthcheck", lambda: Response(status=200))

    kubeflow_adapter = KubeflowAdapter(host=app.config["KUBEFLOW_HOST"],
                                       namespace=app.config["KUBEFLOW_NAMESPACE"],
                                       session_cookie0=app.config["KUBEFLOW_SESSION_COOKIE0"],
                                       session_cookie1=app.config["KUBEFLOW_SESSION_COOKIE1"])

    init_controller(OpenDataDiscoveryController(kubeflow_adapter=kubeflow_adapter,
                                                host=app.config["KUBEFLOW_HOST"]))

    return app


application = create_app(
    os.environ.get("FLASK_CONFIG") or "config.DevelopmentConfig"
)
