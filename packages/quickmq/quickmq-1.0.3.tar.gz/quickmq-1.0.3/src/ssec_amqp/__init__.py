import json
import logging
from contextlib import suppress
from typing import Dict, Optional

import amqp
from amqp.exceptions import MessageNacked
from strenum import StrEnum

from ssec_amqp._defs import (
    AMQP_EXCHANGE_ID_FORMAT,
    DEFAULT_EXCHANGE,
    DEFAULT_PASS,
    DEFAULT_PORT,
    DEFAULT_RECONNECT_WINDOW,
    DEFAULT_USER,
    DEFAULT_VHOST,
    DEFUALT_ROUTE_KEY,
    AMQPConnectionError,
    StateError,
)
from ssec_amqp._utils import NOTYET, RetryInterval, catch_amqp_errors

LOG = logging.getLogger("ssec_amqp")


__all__ = [
    "AmqpExchange",
    "AmqpClient",
    "DeliveryStatus",
    "ConnectionStatus",
]


class DeliveryStatus(StrEnum):
    """Enum for status of messages being delivered"""

    # Message was acknowledged by the server.
    DELIVERED = "DELIVERED"
    # Message was dropped due to reconnection.
    DROPPED = "DROPPED"
    # Message was rejected by the server.
    REJECTED = "REJECTED"


class ConnectionStatus(StrEnum):
    """Enum for status of exchange's connection"""

    # Exchange is connected to the server
    CONNECTED = "CONNECTED"

    # Exchange is reconnecting to the server
    RECONNECTING = "RECONNECTING"

    # Exchange is disconnected from the server
    DISCONNECTED = "DISCONNECTED"


class AmqpExchange:
    """Abstraction of an exchange on a AMQP server."""

    def __init__(
        self,
        host: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        exchange: Optional[str] = None,
        vhost: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        """Initialize the AmqpExchange.

        Args:
            host (str): where the exchange is
            user (str): user to connect with
            password (str): password to connect with
            exchange (Optional[str], optional): name of the exchange. Defaults to None.
            vhost (Optional[str], optional): vhost of the exchange. Defaults to None.
            port (Optional[int], optional): port to connect with. Defaults to None.
        """
        self.host = host
        self.user = user or DEFAULT_USER
        self.vhost = vhost or DEFAULT_VHOST
        self.port = port or DEFAULT_PORT
        self.exchange = exchange or DEFAULT_EXCHANGE
        self.__password = password or DEFAULT_PASS

        # Ignore types for amqp module, as it is untyped itself.
        self.__conn = amqp.Connection(
            f"{self.host}:{self.port}",
            userid=self.user,
            password=self.__password,
            confirm_publish=True,
            connect_timeout=5,
        )
        self.__chan = None  # type: ignore
        self.__chan_id = None

    @property
    def connected(self) -> bool:
        status = self.__conn.connected
        if status is None:
            return False
        return status

    @property
    def identifier(self) -> str:
        return str(self)

    def _channel_open(self) -> bool:
        if not self.connected:
            return False
        return self.__chan is not None and self.__chan.is_open

    @catch_amqp_errors
    def connect(self) -> None:
        """Connects the object to the AMQP exchange using the parameters supplied in constructor."""
        if self.connected:
            return

        if self.__conn.channels is None:
            # Connection previously closed.
            self.__conn = amqp.Connection(
                f"{self.host}:{self.port}",
                userid=self.user,
                password=self.__password,
                confirm_publish=True,
                connect_timeout=5,
            )
        self.__conn.connect()  # type: ignore [attr-defined]
        self.__chan = self.__conn.channel(channel_id=self.__chan_id)  # type: ignore [attr-defined]
        self.__chan_id = self.__chan.channel_id  # type: ignore [attr-defined]

    @catch_amqp_errors
    def produce(self, content_dict, route_key: Optional[str] = None) -> bool:
        """Produce a message to the exchange

        Args:
            content_dict (JSON): The body of the message to produce.
            key (Optional[str], optional): key to send with. Defaults to None.

        Raises:
            AmqpConnectionError: If there is a problem with the connection when publishing.

        Returns:
            bool: Was the message delivered?
        """
        self.refresh()
        content_json = json.dumps(content_dict)
        route_key = route_key or DEFUALT_ROUTE_KEY
        try:
            self.__chan.basic_publish(  # type: ignore [attr-defined]
                msg=amqp.Message(
                    body=content_json,
                    content_type="application/json",
                    content_encoding="utf-8",
                ),
                exchange=self.exchange,
                routing_key=route_key,
                confirm_timeout=5,
            )
        except (MessageNacked, TimeoutError):
            LOG.debug("%s - message was not delivered!", str(self))
            return False
        else:
            return True
        finally:
            if not self._channel_open():  # type: ignore [attr-defined]
                self.__chan = self.__conn.channel(channel_id=self.__chan_id)  # type: ignore [attr-defined]

    @catch_amqp_errors
    def refresh(self) -> None:
        """Refresh the AMQP connection, assure that it is still connected.

        Raises:
            StateError: If the exchange is not connected.
        """
        if self.__conn.connected is None:
            raise StateError(action="refresh", state_info="call connect()")
        try:
            self.__conn.heartbeat_tick()
        except amqp.ConnectionForced:
            self.connect()  # Try again on heartbeat misses

    def close(self) -> None:
        """Closes the connection to the AMQP exchange."""
        self.__conn.collect()

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __repr__(self) -> str:
        return AMQP_EXCHANGE_ID_FORMAT.format(
            user=self.user,
            host=self.host,
            port=self.port,
            vhost=self.vhost,
            exchange=self.exchange,
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return False
        return (
            __value.host == self.host
            and __value.exchange == self.exchange
            and __value.user == self.user
            and __value.port == self.port
            and __value.vhost == self.vhost
        )


# TODO: What to do when exchange disconnects?
class AmqpClient:
    """Client that manages multiple AmqpExchanges at once."""

    def __init__(self, reconnect_window: Optional[float] = None) -> None:
        """Initialize a AmqpClient.

        Args:
            reconnect_window (Optional[float], optional): How long an AmqpExchange
            has to reconnect before an error is raised. Negative for infinite time.
            Defaults to -1.
        """
        self.reconnect_window = reconnect_window or DEFAULT_RECONNECT_WINDOW

        self._connected_pool: list[AmqpExchange] = []
        self._reconnect_pool: dict[AmqpExchange, RetryInterval] = {}

    @property
    def connections(self) -> Dict[str, str]:
        self.refresh_pools()
        d = {exch.identifier: ConnectionStatus.CONNECTED for exch in self._connected_pool}
        d.update({exch.identifier: ConnectionStatus.RECONNECTING for exch in self._reconnect_pool})
        return d

    def connect(self, exchange: AmqpExchange) -> None:
        """Connect this AmqpClient to an AmqpExchange

        Args:
            exchange (AmqpExchange): The AmqpExchange to connect to.

        Raises:
            ConnectionError: If it cannot connect to the exchange.
        """
        LOG.debug("Attempting to connect to %s", str(exchange))

        if exchange in self._connected_pool:
            LOG.debug("Already connected to %s, skipping...", str(exchange))
            return

        if exchange.connected:
            exchange.refresh()
            self._to_connected(exchange)
            return

        try:
            exchange.connect()
        except AMQPConnectionError:
            self._to_reconnect(exchange)
            LOG.info("Initial connection to %s failed, reconnecting", str(exchange))
        else:
            self._to_connected(exchange)
            LOG.debug("Successfully connected to %s", str(exchange))

        self.refresh_pools()  # Could raise a timeout error!

    def publish(self, message, route_key: Optional[str] = None) -> Dict[str, str]:
        """Publish an AMQP message to all exchanges connected to this client.

        Args:
            message (JSONable): A JSON-able message to publish
            route_key (Optional[str], optional): the route key to publish with. Defaults to None.

        Returns:
            Dict[str, DeliveryStatus]: The status of the publish to all exchanges connected to this client.
        """
        status = {}
        self.refresh_pools()
        for exchange in self._connected_pool:
            try:
                routable = exchange.produce(message, route_key)
            except AMQPConnectionError:
                self._to_reconnect(exchange)
            else:
                status[exchange.identifier] = DeliveryStatus.DELIVERED if routable else DeliveryStatus.REJECTED

        # Set status as dropped for all reconnecting exchanges
        status.update({exchange.identifier: DeliveryStatus.DROPPED for exchange in self._reconnect_pool})
        return status

    def disconnect(self, exchange: Optional[AmqpExchange] = None) -> None:
        """Disconnect this AmqpClient from one or all exchanges.

        Args:
            exchange (Optional[AmqpExchange], optional): A specific exchange to disconnect from.
            If none, disconnect from all exchanges. Defaults to None.
        """
        if exchange is not None:
            exchange.close()
            self._reconnect_pool.pop(exchange, None)
            with suppress(ValueError):
                self._connected_pool.remove(exchange)
            return

        for exchange in self._connected_pool:
            exchange.close()
        for exchange in self._reconnect_pool:
            exchange.close()
        self._reconnect_pool.clear()
        self._connected_pool.clear()

    def _to_reconnect(self, exchange: AmqpExchange) -> None:
        """Move an exchange to reconnecting pool.

        Args:
            exchange (AmqpExchange): AmqpExchange to move.
        """
        if exchange in self._connected_pool:
            self._connected_pool.remove(exchange)
        LOG.info("Moving %s to reconnect dict", str(exchange))
        self._reconnect_pool[exchange] = RetryInterval(
            exchange.connect,
            self.reconnect_window,
            (AMQPConnectionError,),
        )

    def _to_connected(self, exchange: AmqpExchange) -> None:
        """Move an exchange to connected pool.

        Args:
            exchange (AmqpExchange): AmqpExchange to move.
        """
        if exchange in self._reconnect_pool:
            del self._reconnect_pool[exchange]
        LOG.info("Moving %s to connected list", str(exchange))
        self._connected_pool.append(exchange)

    def refresh_pools(self) -> None:
        """Refresh this client's pools. Checks if exchanges can reconnect."""
        LOG.debug("Refreshing reconnect pool")
        for exchange, reconnect in self._reconnect_pool.copy().items():
            if reconnect() is NOTYET:
                LOG.debug("%s not yet ready to reconnect", str(exchange))
            else:
                LOG.debug("Moving %s to be connected", str(exchange))
                self._to_connected(exchange)
        for exchange in self._connected_pool:
            try:
                exchange.refresh()
            except AMQPConnectionError:
                LOG.debug("%s is not connected!", str(exchange))
                self._to_reconnect(exchange)
