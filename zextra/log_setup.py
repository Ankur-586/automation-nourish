import logging, pathlib, json, os
import logging.config

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
        separator = "=" * 180
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
    return True #Indicate success

def log_exception(exception):
    """Logs the exception and adds a separator *after* logging."""
    exception_log_path = 'logs/exceptions/app_exceptions.log'  # Define the log file path
    logger = logging.getLogger('exception_logger')  # Get the logger configured for exceptions
    logger.error(exception, exc_info=True)  # Log and check return value
    log_separator(exception_log_path)

setup_logging()
general_logger = logging.getLogger('root')
log_separator('logs/general/general.log')

exception_logger = logging.getLogger('exception_logger')
log_separator('logs/selenium/selenium_general.log')

# exception_logger = logging.getLogger('exception_logger')
# exception_logger.error('This is an error message for the exception logger')


'''
in this code what is happening is that, error is gettitng logged to the exception logger wiht a seperator butn the general and
selenium even though nothing is getting logged to it but still a seperator is geetting added to these log filesa

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

when script runs for the first time and the all file are empty and no exception occurs, then no seperator should be added to the any log files.
when script runs again, then a seperator should be added to the general and selenium because there are already logs statement present.
when scripts run and suppose exception occurs, then the exception_log should get populated. the seperator should get added to the prevoius logs (general and selenium) becasue
        even if there are errors but still some log might get written in them. And on the exception logs no seperator is added as it is its first run.
when script runs again and suppose another exception occurs, the the exception_log should get populated and a seperator should get added as there is a log statement present
when th script runs again and no exception occurs, then the seperator should be added to the general and selenium logs as there are already log statements present.
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
Latest (12:30) 25-12-25 
-------------------------------
First Run (No Exceptions):
No logs have been written yet, so no separators are added to general.log, selenium.log, or app_exceptions.log.
The exception log (app_exceptions.log) remains empty as no exceptions occurred.
First Run (With Exception):

If an exception occurs early in the function (e.g., invalid input such as a non-string product_name), the exception log (app_exceptions.log) will be populated with the exception details.
No separator will be added to app_exceptions.log on this first exception since no prior logs exist.
No separators are added to general.log or selenium.log, as no logging occurred before the exception.
Subsequent Runs (No Exceptions):

Separators will be added to general.log and selenium.log (because they already contain logs from previous runs).
No separator will be added to app_exceptions.log, as no new exception occurred.
Subsequent Runs (With Exceptions):

If an exception occurs, the exception log (app_exceptions.log) will be populated with the exception details.
Separator will be added to app_exceptions.log only if it already contains logs (i.e., it’s not the first exception).
Separators will be added to general.log and selenium.log, as they have logs from previous runs.
Separator Behavior:

No separator should be added to any log file (including app_exceptions.log) if no logs were written earlier in the log file (i.e., it’s the first log entry or the first exception).
Separators should only be added to log files that already contain logs (i.e., once a log entry has been made in the file, separators can be added in subsequent runs).
Key Rules:
First Run (no logs, no exception): No separators.
First Exception (error occurs before any other log entries): No separators added to general.log, selenium.log, or exception.log.
Subsequent Runs (with logs and exception):
Separator added to general.log and selenium.log if logs exist.
Separator added to exception.log only if logs already exist (not on first exception).
This should now match your expectations for separator behavior based on the presence or absence of logs in the files.
'''
'''
i want a logger system in my code that creates 3 log files under diffrent log folder and i want to add
suppose general logs to general.log and all the errors to the exception.log and selenium related to selenium folder
i will share you my log_config.json file
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "json": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "general_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": "logs/general/general.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8"
        },
        "exception_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "logs/exceptions/app_exceptions.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8"
        },
        "selenium_general_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": "logs/selenium/selenium_general.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8"
        },
        "selenium_error_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "logs/selenium/selenium_errors.log",
            "maxBytes": 10485760,
            "backupCount": 3,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": [
                "general_file_handler"
            ],
            "propagate": true
        },
        "exception_logger": {
            "level": "ERROR",
            "handlers": [
                "exception_file_handler"
            ],
            "propagate": false
        },
        "selenium_logger": {
            "level": "DEBUG", 
            "handlers": [
                "selenium_general_handler"
            ],
            "propagate": false
        },
        "selenium.webdriver.common.service": {
            "level": "DEBUG",  
            "handlers": [
                "selenium_general_handler"
            ],
            "propagate": false
        },
        "selenium.webdriver.common.selenium_manager": {
            "level": "DEBUG",  
            "handlers": [
                "selenium_general_handler"
            ],
            "propagate": false
        },
        "selenium.webdriver.remote.remote_connection": {
            "level": "DEBUG",
            "handlers": [
                "selenium_general_handler"
            ],
            "propagate": false
        },
        "urllib3.connectionpool": {
            "level": "DEBUG",  
            "handlers": [
                "selenium_general_handler"
            ],
            "propagate": false
        },
        "selenium_error_logger": {
            "level": "ERROR",  
            "handlers": [
                "selenium_error_handler"
            ],
            "propagate": false
        }
    }
}
'''
