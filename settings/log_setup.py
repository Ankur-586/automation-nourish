import logging, pathlib, json, os
import logging.config

# from settings.log_seperator import log_separator


def ensure_log_folders():
    """Ensures the existence of log folders."""
    log_dir = pathlib.Path('logs')
    subdirs = ['general', 'exceptions', 'selenium']
    log_dir.mkdir(parents=True, exist_ok=True)  # Combined for efficiency
    for subdir in subdirs:
        (log_dir / subdir).mkdir(parents=True, exist_ok=True)

def log_separator(log_file):
    """Adds a separator to the log file if it's not empty."""
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        separator = "==================================================================================================================================="
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

    log_separator('logs/general/general.log')
    log_separator('logs/selenium/selenium_general.log')
    return True #Indicate success

def log_exception(exception):
    """Logs the exception and adds a separator *after* logging."""
    exception_log_path = 'logs/exceptions/app_exceptions.log'  # Define the log file path
    logger = logging.getLogger('exception_logger')  # Get the logger configured for exceptions
    logger.error(f"Exception occurred: {exception}", exc_info=True)  # Log the exception with traceback
    # After logging the exception, add a separator to the log file
    log_separator(exception_log_path)

setup_logging()  # Check if setup was successful
general_logger = logging.getLogger('root')
exception_logger = logging.getLogger('exception_logger')


'''
# def log_separator(log_file):
#     separator_logger = logging.getLogger('separator_logger')
#     # Create a file handler for the specified log file
#     separator_handler = logging.FileHandler(log_file)
#     separator_handler.setFormatter(logging.Formatter('%(message)s'))
#     # Add the handler to the logger
#     separator_logger.addHandler(separator_handler)
#     separator_logger.propagate = False
#     separator_logger.setLevel(logging.DEBUG)
#     # Define the separator string
#     separator = "==================================================================================================================================="
#     # Log the separator to the specified log file
#     separator_logger.debug(separator)
#     # Remove the handler after logging to ensure we don't duplicate it
#     separator_logger.removeHandler(separator_handler)
#     separator_handler.close()
---------------------------------------------
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

In the current implementation,  on the first run a seperator is added to all the log files. Now I have 3 log files in my project.
And generally only 2 log files are getting used in my case is is 1 general log and seleniu and the 3rd one is ony used when there is a exceotion.
Now  suppouse a script run and no error happens thne only the general logfile and selenium log file is used. So definelty the seperator will be added to these 2 files. 
And again if i run the script file again then the seperator will be added to these 2 files again and only if there is a exception then
the seperator should be added to the exception log file. So in this case the seperator will be added to the general and selenium log file again.

--------------------------------------------------------------------------
In the current implementation, a separator is added to all the log files during the first run. My project has three log files: 
one for general logging, one for Selenium logs, and a third for exception logging, which is used only when an exception occurs.
If a script runs without any errors, only the general log file and the Selenium log file are used, so the separator will be added to 
these two files and not the exception but even in that the separeator is getting added. However, if the script is run again, the separator will be added to these same two files again. The separator should
only be added to the exception log file if an exception occurs. In this case, the separator would not be added to the general or 
Selenium log files again.

def log_separator(log_file):
    separator_logger = logging.getLogger('separator_logger')
    # Create a file handler for the specified log file
    separator_handler = logging.FileHandler(log_file)
    separator_handler.setFormatter(logging.Formatter('%(message)s'))
    # Add the handler to the logger
    separator_logger.addHandler(separator_handler)
    separator_logger.propagate = False
    separator_logger.setLevel(logging.DEBUG)
    # Define the separator string
    separator = "==================================================================================================================================="
    # Log the separator to the specified log file
    separator_logger.debug(separator)
    # Remove the handler after logging to ensure we don't duplicate it
    separator_logger.removeHandler(separator_handler)
    separator_handler.close()
    
now the thing is that the seperator is getting added to all the log files by default. but what i want is that when a log file is
called then only a seprator should be added.
i have created 3 log seperators. 
log_separator('logs/general/general.log')
log_separator('logs/selenium/selenium_general.log')
log_separator('logs/exceptions/app_exceptions.log') 

what condition can i put that only adds the seperator when a log file is called

case 1: when script runs for the first time and the all file are empty and no exception occurs, then no seperator should be added to the any log files.
case 2: when script runs again, then a seperator should be added to the general and selenium because there are already logs statement present and if no seperator is there
        then the logs will mix together and will not look good.
case 3: when scripts run and suppose exception occurs, then the exception_log should get populated. the seperator should get added to the prevoius logs becasue
        even if there are errors but still some log might get written in them. And on the exception logs no seperator is added as it is its first riun.
case 4: when script runs and suppose exception occurs, the the exception_log should get populated and a seperator should get added as there is a log statemtn present
        and to make a line between the logs.
case 5: when th script runs again and no exception occurs, then the seperator should be added to the general and selenium logs as there are already log statements present.
        snd no seperator should be added to the exception log as it it is not being triggered.
'''

'''
def log_separator(log_file):
    separator_logger = logging.getLogger('separator_logger')
    # Create a file handler for the specified log file
    separator_handler = logging.FileHandler(log_file)
    separator_handler.setFormatter(logging.Formatter('%(message)s'))
    # Add the handler to the logger
    separator_logger.addHandler(separator_handler)
    separator_logger.propagate = False
    separator_logger.setLevel(logging.DEBUG)
    # Define the separator string
    separator = "==================================================================================================================================="
    # Log the separator to the specified log file
    separator_logger.debug(separator)
    # Remove the handler after logging to ensure we don't duplicate it
    separator_logger.removeHandler(separator_handler)
    separator_handler.close()
    
now the thing is that the seperator is getting added to all the log files by default. but what i want is that when a log file is
called then only a seprator should be added.

case 1: when script runs for the first time and the all file are empty and no exception occurs, then no seperator should be added to the any log files.
case 2: when script runs again, then a seperator should be added to the general and selenium because there are already logs statement present.
case 3: when scripts run and suppose exception occurs, then the exception_log should get populated. the seperator should get added to the prevoius logs (general and selenium) becasue
        even if there are errors but still some log might get written in them. And on the exception logs no seperator is added as it is its first run.
case 4: when script runs again and suppose another exception occurs, the the exception_log should get populated and a seperator should get added as there is a log statement present
case 5: when th script runs again and no exception occurs, then the seperator should be added to the general and selenium logs as there are already log statements present.
        snd no seperator should be added to the exception log as it it is not being triggered.
        '''
'''
You want to add a separator to the log files (general.log, selenium.log, exception.log) under different conditions:

First run: No separators should be added.
Second run (with an exception): A separator should be added to general.log and selenium.log because there is already content, and exception.log should receive a separator as well because an exception occurred.
Subsequent runs (with exceptions): If an exception occurs again, a separator should be added to exception.log (if content exists), and the separator should be added to general.log and selenium.log if content exists.
No exception: If no exception occurs, a separator should be added to general.log and selenium.log if they have content, but not to exception.log.
'''

'''
Latest (17:30)
-------------------------------
You are working with a logging system where you want to add separators to various log files (general, selenium, and exceptions) under specific conditions. The goal is to ensure that separators are added only when appropriate based on whether content already exists in the log files or if an exception occurred during the run.

Expected Behavior:
First Run (No exception):

No separator should be added to any log files, because there is no previous content, and no exception has occurred.
Subsequent Runs (With exception):

A separator should be added to the general and selenium log files only if they contain existing content (i.e., they are not empty).
The app_exceptions.log file should only get a separator if an exception occurred during the current run.
Handling of Exception Logs:

If an exception occurs during the run, the app_exceptions.log should not receive a separator unless it is triggered by an exception during the current run.
Log File Conditions:

A separator should only be added to a file if the file already contains content (i.e., it’s not empty).
The Problem:
The separators are not being added correctly under all conditions.
First run works fine.
Subsequent runs with exceptions: The separator is not being added to app_exceptions.log despite an exception having occurred.
General & Selenium logs should receive a separator only if content exists in them.
'''