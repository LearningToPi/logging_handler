import logging
import logging.handlers
from glob import glob
from datetime import datetime, timedelta
import pathlib
import os

__VERSION__ = (1, 0, 2)

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

_log_level_name = {
    'DEBUG': DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL
}

_supported_log_levels = [DEBUG, INFO, WARNING, ERROR, CRITICAL]


def create_logger(console_level='WARNING', log_file='', file_level='WARNING', name='', file_mode='a', console=True,
                  syslog=False, syslog_script_name='', log_file_vars=[], log_file_retention_days=0, propagate=False):
    """ Creates a logger and returns the handle.
        Log file vars should be sent as a dict -> {"var": "{date}", "set": "%Y-%m-%d-%Y-%M"}

        Supported log file vars:
            {date} - will be replaced with the current date using the provided strftime format
    
     """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = propagate
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(_log_level_name.get(console_level.upper() if not isinstance(console_level, int) else console_level, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # syslog
    if syslog:
        syslog_formatter = logging.Formatter(syslog_script_name + '[%(process)d]: %(levelname)s: %(message)s')
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        syslog_handler.setLevel(_log_level_name.get(file_level.upper() if not isinstance(file_level, int) else file_level, logging.WARNING))
        syslog_handler.setFormatter(syslog_formatter)
        logger.addHandler(syslog_handler)

    # file
    if log_file != '':
        # replace variables in the log file name
        for var in log_file_vars:
            if type(var) == dict and 'var' in var and 'set' in var and var['var'] == "{date}":
                log_file = log_file.replace(var['var'], datetime.now().strftime(var['set']))
        file_handler = logging.FileHandler(log_file, mode=file_mode, encoding='utf-8', delay=False)
        file_handler.setLevel(_log_level_name.get(file_level.upper() if not isinstance(file_level, int) else file_level, logging.WARNING))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # manage retention
        if log_file_retention_days > 0:
            # replace variables with a *
            log_file_search_name = log_file
            for var in log_file_vars:
                log_file_search_name.replace(var['var'], '*')
            old_log_files = glob(log_file_search_name)
            for old_log_file in old_log_files:
                # check the age and delete if needed
                fname = pathlib.Path(old_log_file)
                mtime = datetime.fromtimestamp(fname.stat().st_mtime)
                if mtime < datetime.now() - timedelta(days=log_file_retention_days):
                    logger.info('Deleting old log file %s.  Modified time %s, retention set to %i days.', old_log_file, mtime, log_file_retention_days)
                    os.remove(old_log_file)

    # return the logger
    return logger