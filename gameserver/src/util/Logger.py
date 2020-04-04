import logging


class LogFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        logging.INFO: "\33[34m%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s\33[0m",
        logging.WARNING: "\33[93m%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s\33[0m",
        logging.ERROR: "\33[91m%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s\33[0m",
        logging.CRITICAL: "\33[101m%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s\33[0m"
    }

    def format(self, record):
        logFormat = self.FORMATS[record.levelno]
        formatter = logging.Formatter(logFormat)
        return formatter.format(record)

    @staticmethod
    def getLogger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(LogFormatter())
        logger.addHandler(handler)
        return logger

    @staticmethod
    def debugMode(state):
        logger = logging.getLogger(__name__)
        if state:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)


logger = LogFormatter.getLogger()
