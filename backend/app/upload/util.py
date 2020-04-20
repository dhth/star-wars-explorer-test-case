import datetime
import json
import logging
import os


app_name = os.environ.get("APP_NAME", "Star Wars Explorer Backend")
app_version = os.environ.get("APP_VERSION", "0.0.1")
app_env = os.environ.get("APP_ENV", "development")


def log(log_type: str, **kwargs):
    if log_type == "info":
        level = 200
        level_name = "INFO"
    elif log_type == "error":
        level = 400
        level_name = "ERROR"
    logging_dict = {
        "@timestamp": datetime.datetime.now().isoformat(),
        "application": app_name,
        "version": app_version,
        "environment": app_env,
        "channel": "application",
        "level": level,
        "level_name": level_name,
        "message": kwargs.get("message", ""),
        "context": kwargs.get("context", {}),
    }
    if log_type == "info":
        logging.info(json.dumps(logging_dict))
    elif log_type == "error":
        logging.error(json.dumps(logging_dict))
