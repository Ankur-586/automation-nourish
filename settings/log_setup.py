import logging
import pathlib
import json
import logging.config

def ensure_log_folders():
    '''
    This function ensure the existence of the log folders and their respective log files
    '''
    log_dir = pathlib.Path('logs')
    subdirs = ['general', 'exceptions', 'selenium']
    # Create the base 'logs' directory if it doesn't exist
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created 'logs' directory.")
    # Create subdirectories and corresponding log files
    for subdir in subdirs:
        subdir_path = log_dir / subdir
        if not subdir_path.exists():
            subdir_path.mkdir(parents=True, exist_ok=True)  # Create the subdirectory if it doesn't exist
            print(f"Created folder: {subdir_path}")

def log_separator():
    separator_logger = logging.getLogger('separator_logger')
    separator_handler = logging.FileHandler('logs/general/general.log')
    separator_handler = logging.FileHandler('logs/selenium/selenium_general.log')
    separator_handler = logging.FileHandler('logs/exceptions/app_exceptions.log')
    separator_handler.setFormatter(logging.Formatter('%(message)s'))
    separator_logger.addHandler(separator_handler)
    separator_logger.propagate = False
    separator_logger.setLevel(logging.DEBUG)

    separator = "=============================================================================================================="
    separator_logger.debug(separator)

    separator_logger.removeHandler(separator_handler)
    separator_handler.close()

def setup_logging():
    # Ensure log folders and files exist
    ensure_log_folders()
    # Ensure the 'settings' folder exists
    settings_folder = pathlib.Path('settings')
    if not settings_folder.exists():
        print(f"Error: The 'settings' directory does not exist. Please create it.")
        return 
    # Path to your logging config file (ensure this is correct)
    config_file = settings_folder / 'log_config.json'
    # Check if the config file exists
    if not config_file.exists():
        print(f"Error: Logging configuration file '{config_file}' does not exist.")
        return
    # Load the logging configuration from the JSON file
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)  # Apply logging configuration
        print("Logging configuration loaded successfully.")
    except Exception as e:
        print(f"Error loading logging configuration: {e}")

general_logger = logging.getLogger('root')
exception_logger = logging.getLogger('exception_logger')

setup_logging()
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


  