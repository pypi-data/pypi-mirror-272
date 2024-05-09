# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

import logging

class Logger:

    def __init__(self) -> None:
        self.logger = self.make_logger("ConfigLogger")

    def make_logger(self, name):
        # Create a custom logger
        logger = logging.getLogger(name)

        # Create handlers
        c_handler = logging.StreamHandler()
        # f_handler = logging.FileHandler("file.log")
        i_handler = logging.StreamHandler()
        c_handler.setLevel(logging.WARNING)
        # f_handler.setLevel(logging.ERROR)
        i_handler.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        i_format = logging.Formatter("%(message)s")
        c_handler.setFormatter(c_format)
        # f_handler.setFormatter(f_format)
        i_handler.setFormatter(i_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        # logger.addHandler(f_handler)
        logger.addHandler(i_handler)
        return logger

    def log(self, statement, is_error=False, hash_print=False):
        """Log to the console

        Custom function for Web Application

        Args:
        statement: python object to log on the console
        hash_print: print '-' of size 10 on each side

        Returns:
        None
        """
        if not hasattr(self, "logger"):
            self.logger = self.make_logger("ConfigLogger")
        if is_error:
            self.logger.error(str(statement), exc_info=False, stack_info=False) #change to true in production
        else:
            if hash_print:
                self.logger.info("-" * 10 + str(statement) + "-" * 10)
                print("-" * 10 + str(statement) + "-" * 10)
            else:
                self.logger.info(statement)
                print(statement)
