from flask import current_app as app


def log_error(ex: Exception, context: str):
    app.logger.error('Error in context "' + context + '": ' + str(ex))


def log_warning(message: str):
    app.logger.warning("Warning: " + str)
