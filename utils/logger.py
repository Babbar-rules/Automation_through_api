import logging
import os
from logging.handlers import RotatingFileHandler
import time

class Logger:
    """
    Logger utility for the application.
    """
    
    def __init__(self, name="automation_api", log_dir="logs"):
        """
        Initialize the logger.
        
        Args:
            name: Name of the logger
            log_dir: Directory to store log files
        """
        self.name = name
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        
        # Create file handler with rotation
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5  # 10MB max size, keep 5 backups
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """
        Get the logger instance.
        
        Returns:
            Logger instance
        """
        return self.logger

class FunctionExecutionLogger:
    """
    Special logger for tracking function execution
    """
    
    def __init__(self, log_dir="logs/executions"):
        """
        Initialize the function execution logger.
        
        Args:
            log_dir: Directory to store execution logs
        """
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Main logger
        self.logger = Logger(name="function_executions", log_dir=log_dir).get_logger()
        
    def log_execution(self, function_name, params=None, result=None, error=None, execution_time=None):
        """
        Log function execution details.
        
        Args:
            function_name: Name of the executed function
            params: Parameters passed to the function
            result: Result of the function execution
            error: Error if execution failed
            execution_time: Time taken to execute the function
        """
        log_entry = {
            "function": function_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "params": params if params else "None",
            "execution_time": f"{execution_time:.4f} seconds" if execution_time else "Not measured"
        }
        
        if error:
            log_entry["status"] = "ERROR"
            log_entry["error"] = str(error)
            self.logger.error(f"Function execution failed: {log_entry}")
        else:
            log_entry["status"] = "SUCCESS"
            log_entry["result"] = str(result)
            self.logger.info(f"Function executed successfully: {log_entry}")
            
        return log_entry

# Create singleton instances
app_logger = Logger().get_logger()
execution_logger = FunctionExecutionLogger()

# Convenient functions for logging
def log_info(message):
    app_logger.info(message)

def log_error(message):
    app_logger.error(message)

def log_warning(message):
    app_logger.warning(message)

def log_debug(message):
    app_logger.debug(message)

def log_function_execution(function_name, params=None, result=None, error=None, execution_time=None):
    return execution_logger.log_execution(
        function_name, params, result, error, execution_time
    )
