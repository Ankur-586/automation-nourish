import os
import logging
import pathlib
import json
import logging.config

def ensure_log_folders():
    """Ensures the existence of log folders."""
    log_dir = pathlib.Path('logs')
    subdirs = ['general', 'exceptions', 'selenium']
    log_dir.mkdir(parents=True, exist_ok=True)  # Combined for efficiency
    for subdir in subdirs:
        (log_dir / subdir).mkdir(parents=True, exist_ok=True)

def log_separator(log_file):
    """Adds a separator to the log file if it's empty or missing."""
    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(log_file):
        with open(log_file, 'w'):  # Create an empty file
            pass
    separator = "=" * 180
    if os.path.getsize(log_file) == 0:
        with open(log_file, 'a') as f:
            f.write(f"\n{separator}\n")
    else:
        with open(log_file, 'a') as f:
            f.write(f"\n{separator}\n")

def setup_logging():
    ensure_log_folders()
    settings_folder = pathlib.Path('settings')
    if not settings_folder.exists():
        print("Error: The 'settings' directory does not exist.")
        return False  # Indicate failure
    config_file = settings_folder / 'log_config.json'
    if not config_file.exists():
        print(f"Error: Logging configuration file '{config_file}' does not exist.")
        return False  # Indicate failure
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    except (json.JSONDecodeError, FileNotFoundError) as e: # More specific exception handling
        print(f"Error loading logging configuration: {e}")
        return False  # Indicate failure

    # Ensure separator is added to all log files at setup
    log_separator('logs/general/general.log')
    log_separator('logs/selenium/selenium_general.log')
    return True  # Indicate success

def log_exception(exception):
    """Logs the exception and adds a separator *after* logging."""
    exception_log_path = 'logs/exceptions/app_exceptions.log'  # Define the log file path
    logger = logging.getLogger('exception_logger')  # Get the logger configured for exceptions
    logger.error(exception, exc_info=True)  # Log the exception
    log_separator(exception_log_path)  # Add a separator after logging the exception

setup_logging()
general_logger = logging.getLogger('root')
exception_logger = logging.getLogger('exception_logger')


# def log_exception(exception):
#     """Logs the exception and adds a separator *after* logging."""
#     exception_log_path = 'logs/exceptions/app_exceptions.log'  # Define the log file path
#     logger = logging.getLogger('exception_logger')  # Get the logger configured for exceptions
#     logger.error(exception, exc_info=True)  # Log and check return value
#     log_separator(exception_log_path)

# def log_separator(log_file):
#     """Adds a separator to the log file if it's not empty."""
#     if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
#         separator = "=" * 180
#         with open(log_file, 'a') as f:
#             f.write(f"\n{separator}\n")