from flask import Flask

from ucam_faas import FaaSGunicornApplication


def test_faas_gunicorn_application_setup():
    app = Flask(__name__)

    application = FaaSGunicornApplication(app, "0.0.0.0", "8080")

    # Set by __init__:
    assert application.cfg.bind == ["0.0.0.0:8080"]
    # Read from the default 'gunicorn.conf.py' file:
    assert application.cfg.logconfig_dict["version"] == 1
    assert (
        len(application.cfg.logconfig_dict["formatters"]["json_formatter"]["foreign_pre_chain"])
        == 3
    )
