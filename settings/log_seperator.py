import logging
import pathlib
import time

class SeparatorLogHandler(logging.Handler):
    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

    def emit(self, record):
        # Check if the file is non-empty or modified recently
        if self.log_file.stat().st_size > 0:  # Non-empty file
            separator = "=============================================================================================================="
            with open(self.log_file, 'a') as f:
                f.write(f"{separator}\n")  # Add the separator before writing the log

        # Proceed with the regular log writing
        with open(self.log_file, 'a') as f:
            f.write(self.format(record) + "\n")


def log_separator():
    '''
    This function adds a separator to all non-empty or recently modified log files
    whenever a log is triggered.
    '''
    log_dir = pathlib.Path('logs')
    # Create a list of all log files in the subdirectories
    log_files = []
    for subdir in log_dir.iterdir():
        if subdir.is_dir():  # Check if it's a subdirectory
            for log_file in subdir.glob('*.log'):  # Find all .log files in the subdir
                log_files.append(log_file)
    
    if not log_files:
        print("No log files found to add a separator.")
        return

    # Set up a logger to write the separator
    separator_logger = logging.getLogger('separator_logger')
    separator_logger.setLevel(logging.DEBUG)  # Set the level to DEBUG
    
    # Define a formatter for the separator (if any)
    formatter = logging.Formatter('%(message)s')

    # Add the custom handler to each log file
    for log_file in log_files:
        if log_file.stat().st_size > 0 or (time.time() - log_file.stat().st_mtime) < 3 * 24 * 60 * 60:  # 3 days threshold for recently modified
            handler = SeparatorLogHandler(log_file)
            handler.setFormatter(formatter)
            separator_logger.addHandler(handler)

    # Write a test log that will trigger the separator
    # separator_logger.debug("This is a log entry triggering the separator.")

    # Clean up handlers after logging to avoid duplicate entries
    for handler in separator_logger.handlers:
        separator_logger.removeHandler(handler)
        handler.close()

    print("Separator triggered in log files.")

