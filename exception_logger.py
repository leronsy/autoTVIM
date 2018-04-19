import logging

import functools
import time
def exception(ecx_logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param ecx_logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "Ошибка в "
                err += func.__name__
                ecx_logger.exception(err)

                # re-raise the exception
                raise

        return wrapper

    return decorator



def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler

    timestr = time.strftime("%y.%m.%d %H-%M")
    fh = logging.FileHandler("test"+timestr+".log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = create_logger()



