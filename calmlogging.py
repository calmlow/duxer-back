# Own logging module, custom colorized style formatting, braces style support
#
#
import logging


class color:
    """ The ansi colors """
    NOFORMAT = '\033[0m'
    LIGHTGREEN = '\033[1;32m'
    ORANGE = '\033[0;33m'
    U_ORANGE = '\033[4;33m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    LIGHTBLUE = '\033[1;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    ITALIC = '\033[3;37m'
    GRAY = '\033[2;37m'
    GRAY_IT = '\033[3;37m'


class BraceMessage(object):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        try:
            return self.msg.format(*self.args, **self.kwargs)
        except Exception as exc:
            return "Error in message formatting\n    .format({}, *{}, **{})\n{}: {}".format(
                repr(self.msg), self.args, self.kwargs,
                type(exc).__name__, str(exc))


class BraceLogger(logging.getLoggerClass()):
    # Don't allow below reserved named attributes to be passed
    _reserved = (('exc_info', None), ('extra', None), ('stack_info', False))

    def _log(self, level, msg, args, **kwargs):
        d = {k: kwargs.pop(k, v) for k, v in self._reserved}
        return super()._log(
            level, BraceMessage(msg, *args, **kwargs), (), **d)

    @classmethod
    def getLogger(_, name):
        logger = logging.getLogger(name)
        logger.__class__ = __class__
        return logger


class CustomFormatter(logging.Formatter):
    format_full = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    format_info = f'{color.LIGHTBLUE}[%(levelname)s]{color.NOFORMAT}\t  %(asctime)s - %(message)s \t{color.U_ORANGE}(%(filename)s:%(lineno)d){color.NOFORMAT}'
    format_debug = f'{color.BLUE}[%(levelname)s]{color.NOFORMAT}\t  %(asctime)s - %(message)s \t{color.U_ORANGE}(%(filename)s:%(lineno)d){color.NOFORMAT}'
    format_warn = f'{color.ORANGE}[%(levelname)s]{color.NOFORMAT} %(asctime)s - %(message)s \t{color.U_ORANGE}(%(filename)s:%(lineno)d){color.NOFORMAT}'
    format_error = f'{color.RED}[%(levelname)s]{color.NOFORMAT}\t  %(asctime)s - %(message)s \t{color.U_ORANGE}(%(filename)s:%(lineno)d){color.NOFORMAT}'
    format_critical = f'{color.RED}[%(levelname)s]{color.NOFORMAT}%(asctime)s - %(message)s \t{color.U_ORANGE}(%(filename)s:%(lineno)d){color.NOFORMAT}'

    format_nocolors = '[%(levelname)s]\t  %(asctime)s - %(name)s - %(message)s'
    format_notime = '[%(levelname)s]\t  %(name)s - %(message)s'

    use_color = True

    FORMATS = {
        logging.DEBUG: format_debug,
        logging.INFO: format_info,
        logging.WARNING: format_warn,
        logging.ERROR: format_error,
        logging.CRITICAL: format_critical
    }

    def __init__(self, use_color=True):
        self.use_color = use_color
        super().__init__(self.format_nocolors)

    def format(self, record):
        log_format_corresponding_level = self.FORMATS.get(record.levelno)
        if self.use_color:
            # Replace the original format with one customized by logging level
            super().__init__(log_format_corresponding_level)
        return super().format(record)


def get_logger(name='root'):
    import sys
    customerLogger = BraceLogger.getLogger(name)
    customerLogger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    customFormatter = CustomFormatter(use_color=True)
    handler.setFormatter(customFormatter)
    customerLogger.addHandler(handler)

    return customerLogger


if __name__ == '__main__':
    """ Test the logger independently. This module was developed with
        Python 3.8 and works for that Logging package.
    """
    log = get_logger('test')
    log.info('{}: {first} {last} has email {email}', 'User',
             first='Joe', last='Doe', email='joe.doe@example.com')
    log.warning('The yellow warning!')
    log.error("Error from the /health endpoint")
    log.debug("Debug from the {endpoint} endpoint.", endpoint='/health')
    log.critical("Critical from the /health endpoint")
