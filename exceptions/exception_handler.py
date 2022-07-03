import functools
import logging

from rest_framework.exceptions import ValidationError

logger = logging.getLogger('sicaf_middleware.apps')


def helper_exceptions(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exception:
            logger.error(f"Exception handler - ValidationError caught: {exception}")
            raise exception
        except Exception as exception:
            logger.error(f"Exception handler - Exception caught: {exception}")
            raise exception
    return wrapper
