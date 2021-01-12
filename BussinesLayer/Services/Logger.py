import logging


logging.basicConfig(filename="visualizeBguLogs.log", format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)


def info(msg):
    logger.info(", INFO: " + msg)


def error(msg):
    logger.error(", ERROR: " + msg)
