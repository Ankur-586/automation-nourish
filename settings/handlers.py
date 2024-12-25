# handlers.py
import logging

class RequestSeparatorHandler(logging.Handler):
    """Custom handler to add separator after a full set of log messages for a request."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = "====================================================================================================================\n"
    
    def emit(self, record):
        """Emit a log record and append a separator after every complete request log."""
        try:
            log_message = self.format(record)
            # Print log message
            print(log_message)
            # Add the separator after the full group of request logs
            if record.levelname == "INFO":  # Assuming logs for a request are at the INFO level
                print(self.separator)
        except Exception:
            self.handleError(record)
            

