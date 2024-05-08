"""
ssec_amqp._utils
~~~~~~~~~~~~~~~~

Internal utility classes/functions.
"""

import time

from amqp import Connection

from ssec_amqp._defs import AMQPConnectionError, RetryTimeoutError


class NotYet:
    """Sentinal class for when a retry is not yet ready"""


# Sentinal to use for RetryInterval
NOTYET = NotYet()


class RetryInterval:
    def __init__(self, action, total_interval: float, errors=(Exception)) -> None:
        self._init_time = time.time()

        self.action = action
        self.errors = errors
        self.total_interval = total_interval

        if total_interval < 0:
            self._max_time = float("inf")
        else:
            self._max_time = self._init_time + total_interval

    def __call__(self) -> NotYet:
        cur_time = time.time()

        try:
            return self.action()
        except self.errors as e:
            if cur_time >= self._max_time:
                raise RetryTimeoutError(self.total_interval) from e
            return NOTYET


def catch_amqp_errors(func):
    """Utility decorator to catch all of Pika's AMQPConnectionError and
    raise them as built-in ConnectionError

    Args:
        func (Callable): Function to decorate
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Connection.recoverable_connection_errors as e:
            raise AMQPConnectionError from e

    return wrapper
