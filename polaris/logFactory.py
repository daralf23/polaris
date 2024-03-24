import logging, platform
import logging.handlers
import requests
import json
import os

def logFactory(name):
    returnLogger = logging.getLogger(name)
    returnLogger.setLevel(logging.INFO)
    log_format = "[{asctime}] [{levelname:<8}] {name:<16}: {message}"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format, style="{")

    if 'console' in os.environ['LOG_CONFIG']:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        if (int(os.environ['DEBUG']) == 1): 
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.INFO)
        returnLogger.addHandler(console_handler)

    if 'file' in os.environ['LOG_CONFIG']:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f"{os.environ['LOG_PATH']}/bot.log",
            encoding="utf-8",
            maxBytes=32 * 1024 * 1024,
            backupCount=5,
        )

        file_handler_error = logging.handlers.RotatingFileHandler(
            filename=f"{os.environ['LOG_PATH']}/bot_error.log",
            encoding="utf-8",
            maxBytes=32 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        file_handler_error.setFormatter(formatter)

        file_handler.setLevel(logging.INFO)
        file_handler_error.setLevel(logging.ERROR)

        returnLogger.addHandler(file_handler)
        returnLogger.addHandler(file_handler_error)

        if (int(os.environ['DEBUG']) == 1): 
            returnLogger.setLevel(logging.DEBUG)

    if 'database' in os.environ['LOG_CONFIG']:
        pass
    
    return returnLogger