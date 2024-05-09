import logging

class Logger:

    def __init__(self) -> None:
        self.logger = self.make_logger("ConfigLogger")

    def make_logger(self, name):
        # Create a custom logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.ERROR)  # Set the logger to handle only errors

        # Create file handler for errors
        f_handler = logging.FileHandler("error.log")  # File handler for errors
        f_handler.setLevel(logging.ERROR)  # File handler captures only errors

        # Create formatter and add it to handler
        f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        f_handler.setFormatter(f_format)

        # Add handler to the logger
        logger.addHandler(f_handler)

        # Disable propagation to avoid logging errors to console through default handlers
        logger.propagate = False

        return logger


    def log(self, statement, is_error=False, hash_print=False):
        """Log to the console or file based on the log type

        Args:
            statement: Python object to log on the console or file
            is_error: Flag to determine if it's an error log
            hash_print: Print '-' of size 10 on each side

        Returns:
            None
        """
        if not hasattr(self, "logger"):
            self.logger = self.make_logger("ConfigLogger")
        if is_error:
            self.logger.error(str(statement), exc_info=False, stack_info=False)  # Log error to file only
        else:
            if hash_print:
                decorated_statement = "-" * 10 + str(statement) + "-" * 10
                self.logger.info(decorated_statement)
                print(decorated_statement)
            else:
                self.logger.info(statement)
                print(statement)
