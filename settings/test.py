import pathlib
import json
import logging
import logging.config


class RequestSeparatorHandler(logging.Handler):
    """Custom handler to add separator after a log message."""

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename  # Store the filename
        self.separator = "====================================================================================================================\n"

    def emit(self, record):
        """Emit a log record and append a separator."""
        try:
            log_message = self.format(record)
            with open(self.filename, 'a') as f: # Open the file for appending
                f.write(log_message + '\n') # Write the log message and a newline
                if record.levelname == "INFO": # Check if the log level is INFO
                    f.write(self.separator)  # Write separator to the file
        except Exception:
            self.handleError(record)

def ensure_log_folders():
    """Ensures the existence of log folders."""
    log_dir = pathlib.Path('logs')
    subdirs = ['general', 'exceptions', 'selenium']
    log_dir.mkdir(parents=True, exist_ok=True)  # Combined for efficiency
    for subdir in subdirs:
        (log_dir / subdir).mkdir(parents=True, exist_ok=True)

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

        # Add the custom separator handler in the handlers section
        config['handlers']['request_separator_handler'] = {
            'level': 'INFO',  # Only for INFO level logs
            'class': 'settings.handlers.RequestSeparatorHandler',  # Full path to the custom handler
            'formatter': 'separator',  # Name of the formatter to use
            'stream': 'ext://sys.stdout'  # Standard output for the separator to be printed
        }

        # Apply the custom separator formatter
        config['formatters']['separator'] = {
            '()': 'logging.Formatter',  # Use the built-in Formatter as a base class
            'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # The actual format
        }

        # Apply the updated configuration
        logging.config.dictConfig(config)

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading logging configuration: {e}")
        return False  # Indicate failure
    return True  # Indicate success

# Run the setup
if setup_logging():
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