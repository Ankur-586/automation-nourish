import logging, pathlib, json, time
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
    # Create subdirectories and corresponding log files
    for subdir in subdirs:
        subdir_path = log_dir / subdir
        if not subdir_path.exists():
            subdir_path.mkdir(parents=True, exist_ok=True)  # Create the subdirectory if it doesn't exist

def log_separator():
    '''
    This function adds a separator to all non-empty or recently modified log files
    whenever a log is triggered.
    '''
    log_dir = pathlib.Path('logs')
    # Create a list of all log files in the subdirectories
    log_files = []
    # Find all .log files in the subdirectories
    for subdir in log_dir.iterdir():
        if subdir.is_dir():  # Check if it's a subdirectory
            for log_file in subdir.glob('*.log'):  # Find all .log files in the subdir
                log_files.append(log_file)
    if not log_files:
        print("No log files found to add a separator.")
        return
    # Separator line to add
    separator = "=============================================================================================================="
    # Loop through all the log files and add separator if necessary
    for log_file in log_files:
        # Check if the log file is non-empty or recently modified
        if log_file.stat().st_size > 0 or (time.time() - log_file.stat().st_mtime) < 3 * 24 * 60 * 60:  # Recently modified (3 days)
            # Open the log file and add a separator before writing a log
            with open(log_file, 'a') as f:
                f.write(f"{separator}\n")  # Add separator

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
    except Exception as e:
        print(f"Error loading logging configuration: {e}")

general_logger = logging.getLogger('root')
exception_logger = logging.getLogger('exception_logger')
setup_logging()
log_separator()  

'''
In the code the core logic is that add the seperator if file is non-empty.
but we can also so like, suppose whenever a log file is triggered,
then the the seperator should be added else not. but the issue is that how do we know when a log 
file is triiggered.

# def log_separator():
#     
#     This function writes a separator to only the log files that have been modified recently or are non-empty.
#     
#     log_dir = pathlib.Path('logs')
#     # Create a list of all log files in the subdirectories
#     log_files = []
#     for subdir in log_dir.iterdir():
#         if subdir.is_dir():  # Check if it's a subdirectory
#             for log_file in subdir.glob('*.log'):  # Find all .log files in the subdir
#                 log_files.append(log_file)
#     if not log_files:
#         print("No log files found to add a separator.")
#         return
#     # Set up a logger to write the separator
#     separator_logger = logging.getLogger('separator_logger')
#     separator_logger.setLevel(logging.DEBUG)  # Set the level to DEBUG
#     # Define a formatter for the separator
#     formatter = logging.Formatter('%(message)s')
#     # Add a handler for each log file dynamically (but only for used/modified files)
#     handlers = []
#     for log_file in log_files:
#         if log_file.stat().st_size > 0:  # Only proceed if the file is non-empty
#             handler = logging.FileHandler(log_file)
#             handler.setFormatter(formatter)
#             handlers.append(handler)
#             separator_logger.addHandler(handler)
#         else:
#             # If the file is empty, check its modification time and log only if it's recently modified
#             last_modified_time = log_file.stat().st_mtime
#             # You can adjust the threshold for "recently modified" (e.g., 3 days ago)
#             if (time.time() - last_modified_time) < 3 * 24 * 60 * 60:  # 3 days in seconds
#                 handler = logging.FileHandler(log_file)
#                 handler.setFormatter(formatter)
#                 handlers.append(handler)
#                 separator_logger.addHandler(handler)
#     separator_logger.propagate = False  # Don't propagate to the root logger
#     # Define the separator string
#     separator = "=============================================================================================================="
#     # Log the separator to each handler
#     separator_logger.debug(separator)
#     # Remove handlers after logging to prevent duplicate log entries
#     for handler in handlers:
#         separator_logger.removeHandler(handler)
#         handler.close()
#     print(f"Separator logged to {len(handlers)} log files.")
'''


  