"""
rviclog.py
"""
import logging
import os
import sys
from time import gmtime, strftime

# -------------------------------------------------------------------- #
log_name = 'rvic'
formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(message)s')
# -------------------------------------------------------------------- #


# -------------------------------------------------------------------- #
# Fake stream file to handle stdin/stdout
class StreamToFile(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
    """
    def __init__(self, logger_name=log_name, log_level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
# -------------------------------------------------------------------- #


# -------------------------------------------------------------------- #
# Function to start logging
def init_logger(logDir='./', log_level='DEBUG', verbose=False):
    """ Setup the logger """

    log_file = os.path.join(logDir, 'RVIC-'+strftime("%Y%m%d-%H%M%S", gmtime())+'.log')
    print 'Log File:  %s' % log_file
    print 'Logging To Console: %s' % verbose

    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    logger.propograte = True

    # ---------------------------------------------------------------- #
    # create log file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.filename = log_file
    # ---------------------------------------------------------------- #

    # ---------------------------------------------------------------- #
    # If verbose, logging will also be sent to console
    if verbose:
        # print to console
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    # ---------------------------------------------------------------- #

    # ---------------------------------------------------------------- #
    # Redirect stdout and stderr to logger
    sys.stdout = StreamToFile()
    sys.stderr = StreamToFile(log_level=logging.ERROR)
    # ---------------------------------------------------------------- #

    logger.info('--------------------- INITIALIZED RVIC LOG ---------------------')
    logger.info('LOG LEVEL: %s' % log_level)

    return logger
# -------------------------------------------------------------------- #