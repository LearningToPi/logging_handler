'''
MIT License

Copyright (c) 2022 LearningToPi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import logging
import logging.handlers
from glob import glob
from datetime import datetime, timedelta
import pathlib
import os

__VERSION__ = (1, 0, 7)

DEFAULT_LEVEL = logging.WARNING

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'

_log_level_number = {
    'DEBUG': logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


def create_logger(console_level=WARNING, log_file='', file_level=WARNING, name='', file_mode='a', console=True,
                  syslog=False, syslog_script_name='', log_file_vars=None, log_file_retention_days=0, propagate=False):
    """ Creates a logger and returns the handle.
        Log file vars should be sent as a list of dict -> [{"var": "{date}", "set": "%Y-%m-%d-%Y-%M"}]

        Supported log file vars:
            {date} - will be replaced with the current date using the provided strftime format
    
     """
    logger = logging.getLogger(name)
    logger.handlers.clear() # Clear all existing handlers before creating new ones!
    logger.setLevel(logging.DEBUG)
    logger.propagate = propagate
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level if isinstance(console_level, int) else _log_level_number.get(str(console_level).upper(), DEFAULT_LEVEL))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # syslog
    if syslog:
        syslog_formatter = logging.Formatter(syslog_script_name + '[%(process)d]: %(levelname)s: %(message)s')
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        syslog_handler.setLevel(file_level if isinstance(file_level, int) else _log_level_number.get(str(file_level).upper(), DEFAULT_LEVEL))
        syslog_handler.setFormatter(syslog_formatter)
        logger.addHandler(syslog_handler)

    # file
    if log_file != '':
        # replace variables in the log file name
        if log_file_vars is not None:
            for var in log_file_vars:
                if isinstance(var, dict) and 'var' in var and 'set' in var and var['var'] == "{date}":
                    log_file = log_file.replace(var['var'], datetime.now().strftime(var['set']))
        file_handler = logging.FileHandler(log_file, mode=file_mode, encoding='utf-8', delay=False)
        file_handler.setLevel(file_level if isinstance(file_level, int) else _log_level_number.get(str(file_level).upper(), DEFAULT_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # manage retention
        if log_file_retention_days > 0:
            # replace variables with a *
            log_file_search_name = log_file
            if log_file_vars is not None:
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
