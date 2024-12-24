import pathlib
import json
import logging
import logging.config

def ensure_log_folders():
    """Ensures the existence of log folders."""
    log_dir = pathlib.Path('logs')
    subdirs = ['general', 'exceptions', 'selenium']
    log_dir.mkdir(parents=True, exist_ok=True)
    for subdir in subdirs:
        (log_dir / subdir).mkdir(parents=True, exist_ok=True)

def log_separator(log_path):
    """Adds a separator to the log file if it is not empty."""
    if log_path.exists() and log_path.stat().st_size > 0:  # Check if file is not empty
        with open(log_path, 'a') as f:
            separator = "=============================================================================================================="
            f.write(f"\n{separator}\n")

def log_exception(exception):
    """Logs the exception to the exception log file."""
    logger = logging.getLogger('exception_logger')
    logger.exception(exception)

def setup_logging():
    ensure_log_folders()  # Ensure that the required log directories exist
    settings_folder = pathlib.Path('settings')
    
    if not settings_folder.exists():
        print("Error: The 'settings' directory does not exist.")
        return False
    
    config_file = settings_folder / 'log_config.json'
    
    if not config_file.exists():
        print(f"Error: Logging configuration file '{config_file}' does not exist.")
        return False
    
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)  # Set up logging based on the config
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading logging configuration: {e}")
        return False

    # Log file paths
    general_log_path = pathlib.Path('logs/general/general.log')
    selenium_log_path = pathlib.Path('logs/selenium/selenium_general.log')
    exception_log_path = pathlib.Path('logs/exceptions/app_exceptions.log')

    # Log separators
    log_separator(general_log_path)
    log_separator(selenium_log_path)

    return True

setup_logging()