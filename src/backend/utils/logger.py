"""The logger module provides wrapper functions to log errors and warnings."""

from flask import current_app as app


def log_error(ex: Exception, context: str):
    """Log a caught exception.

    :param ex: The thrown exception.
    :param context: The context in which the exception was thrown.
    """
    app.logger.error('Error in context "' + context + '": ' + str(ex))


def log_warning(message: str):
    """Log a warning message.

    :param message: The warning message.
    """
    app.logger.warning("Warning: " + str)
