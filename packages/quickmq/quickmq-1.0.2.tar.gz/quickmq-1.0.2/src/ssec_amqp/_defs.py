"""
ssec_amqp._defs
~~~~~~~~~~~~~~~

Definitions that are used in ssec_amqp.
"""

from typing import Optional

# Inspired by the AMQP URI format, and adds the exchange to the end
AMQP_EXCHANGE_ID_FORMAT = "amqp://{user:s}@{host:s}:{port:d}{vhost:s}/{exchange:s}"

# Default AmqpExchange values
DEFAULT_USER = "guest"
DEFAULT_PASS = "guest"  # noqa: S105
DEFAULT_PORT = 5672
DEFAULT_VHOST = "/"
DEFAULT_EXCHANGE = ""
DEFUALT_ROUTE_KEY = ""

# Default AmqpClient values
DEFAULT_RECONNECT_WINDOW = -1.0  # reconnects forever


# Exceptions that are used within ssec_amqp
class StateError(Exception):
    """Wrong state to perform an action."""

    def __init__(self, action: str, state_info: Optional[str]) -> None:
        msg = f"Cannot perform {action} in this state"
        if state_info is None:
            msg += "!"
        else:
            msg += f"({state_info})!"
        super().__init__(msg)


class RetryTimeoutError(TimeoutError):
    """Reconnect retrying timed out."""

    def __init__(self, time: float) -> None:
        super().__init__(f"Could not reconnect after {time} seconds!")


class AMQPConnectionError(ConnectionError):
    """All purpose error for any problems with the AMQP connection."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
