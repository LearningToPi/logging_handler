# Python Logging Helper
Python library to quickly create logging handlers.  Supports logging to the console as well as to file using a syslog style output format.

## Installation
The package is available on PyPi or can be installed manually using the why/tar.gz file attached to the release.

    pip3 install logging_helper

## Introduction
This library provides a function called "create_logger" that will create and return a logging handler that can be used in your application.  The "create_logger" function can be passed a series of different settings to manipulate the default Python logging handler.

## Examples

    >>> from logging_helper import create_logger
    >>> logger = create_logger(console=True)
    >>> logger.warning('test')
    2022-11-09 16:09:21,210 - root - WARNING - test
    >>>
    >>> logger.debug('test debug')
    >>> ### Note no output! Default is set to WARNING and above
    >>>
    >>> logger = create_logger(console=True, console_level='DEBUG')
    >>> logger.debug('test debug')
    2022-11-09 16:11:13,268 - root - DEBUG - test debug
    >>> 
    >>> logger2 = create_logger(console=True, console_level='DEBUG', name='log2')
    >>> logger2.info('logger2 info!')
    2022-11-09 16:12:23,358 - log2 - INFO - logger2 info!
    >>> logger.info('logger1 info!')
    2022-11-09 16:12:35,510 - root - INFO - logger1 info!

In the examples above, you can create multiple loggers with different names.  If a name is not provided, the logger takes on the 'root' logger for Python.  Replacing the 'root' logger will replace the default logging in python and affects other modules.  If you set your logger to debug and start seeing messages from other modules you weren't expecting, provide a name value to your logger.

## Parameters
| Parameter | Default | Description |
| --------- | ------- | ----------- |
| console_level | 'INFO' (str) | Set the logging level for the console
| console | True (bool) | Enable / Disable logging to the console
| log_file | '' (str) | Set the file to log to (blank means none)
| file_level | 'WARNING' (str) | Set the logging level for the file
| file_mode | 'a' (str) | Feeds into the file mode 'a' for append, 'w' for overwrite
| name | '' (str) | Name for the logger. Blank will replace the root logging handler
| syslog | False (bool) | Send messages to the local system logger
| syslog_script_name | '' (str) | Name to include when using the local system logger
| log_file_vars | [] (list) | list of variables that can be used to create the log file names
| log_file_retention_days | 0 (int) | Specify the max number of days to retain the log files
| propagate | False (bool) | If set to true, the named loggers will also be processed by the root logger.  Generally leave false

## Release Notes

Release notes can now be found in the release notes folder.

## Changing Logging Level

As of v1.0.8, two functions, "update_console_level" and "update_file_level" have been added.  To change the logging level on the fly:

    >>> from logging_helper import create_logger, update_console_level
    >>> logger = create_logger(console=True)
    >>> update_console_level(logger, 'info')

## CustomLogger class

As of v1.0.8, a CustomLogger class was added.  This performs the same function as using create_logger, however rather than requiring a separate function to update logging levels, the class includes a "console_level" and "file_level" function that can be used.  The class also utilizes threading to enable old logfile cleanup.
