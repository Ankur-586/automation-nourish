import logging
import pathlib
import json
import logging.config

def log_separator():
    separator_logger = logging.getLogger('separator_logger')
    separator_handler = logging.FileHandler('logs/my_app.log')
    separator_handler.setFormatter(logging.Formatter('%(message)s'))
    separator_logger.addHandler(separator_handler)
    separator_logger.propagate = False
    separator_logger.setLevel(logging.DEBUG)

    separator = "=============================================================================================================="
    separator_logger.debug(separator)

    separator_logger.removeHandler(separator_handler)
    separator_handler.close()

# logging
def setup_logging():
    config_file = pathlib.Path(r"settings/log_config.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

setup_logging()
logger = logging.getLogger(__name__)
log_separator()


'''
Do Not Delete

def log_separator():
    separator_logger = logging.getLogger('separator_logger')
    separator_handler = logging.FileHandler('logs/my_app.log')
    separator_handler.setFormatter(logging.Formatter('%(message)s'))
    separator_logger.addHandler(separator_handler)
    separator_logger.propagate = False
    separator_logger.setLevel(logging.DEBUG)

    separator = "=============================================================================================================="
    separator_logger.debug(separator)

    separator_logger.removeHandler(separator_handler)
    separator_handler.close()

# logging
def setup_logging():
    config_file = pathlib.Path(r"settings/log_config.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

log config.py


i want that if i get a exception in my application then the excption should be shown in a seperate log file.
if not exception and everythngs works as expected then seperate log file should get populated 
and if i get a seenium error then a seperate log file should get populated
'''