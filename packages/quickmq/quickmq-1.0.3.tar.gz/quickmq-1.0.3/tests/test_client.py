from unittest import mock

import ssec_amqp as mq
from ssec_amqp._defs import DEFAULT_RECONNECT_WINDOW, AMQPConnectionError
from ssec_amqp._utils import NOTYET


def is_reconnecting(client: mq.AmqpClient, exchange: mq.AmqpExchange) -> bool:
    return client.connections.get(exchange.identifier) == mq.ConnectionStatus.RECONNECTING


def is_connected(client: mq.AmqpClient, exchange: mq.AmqpExchange) -> bool:
    return client.connections.get(exchange.identifier) == mq.ConnectionStatus.CONNECTED


def is_disconnected(client: mq.AmqpClient, exchange: mq.AmqpExchange) -> bool:
    return not (is_reconnecting(client, exchange) or is_connected(client, exchange))


def test_init():
    cl = mq.AmqpClient()
    assert cl.connections == {}
    assert cl.reconnect_window == DEFAULT_RECONNECT_WINDOW

    new_window = 20
    cl = mq.AmqpClient(new_window)
    assert cl.connections == {}
    assert cl.reconnect_window == new_window


def test_connect_err():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connect.side_effect = AMQPConnectionError
        mock_exch.connected = False
        cl.connect(mock_exch)
        assert is_reconnecting(cl, mock_exch)


def test_connect():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = False
        cl.connect(mock_exch)
        mock_exch.connect.assert_called_once()
        assert is_connected(cl, mock_exch)
        assert not is_reconnecting(cl, mock_exch)


def test_exch_already_connected():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = True
        cl.connect(mock_exch)
        mock_exch.connect.assert_not_called()
        assert is_connected(cl, mock_exch)
        assert not is_reconnecting(cl, mock_exch)


def test_already_connected():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        assert not is_connected(cl, mock_exch)
        mock_exch.connected = True
        cl.connect(mock_exch)
        cl.connect(mock_exch)
        mock_exch.connect.assert_not_called()
        assert is_connected(cl, mock_exch)


def test_connect_when_reconnecting():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = False
        cl.connect(mock_exch)
        mock_exch.refresh.side_effect = AMQPConnectionError
        cl.refresh_pools()
        assert is_reconnecting(cl, mock_exch)
        mock_exch.connect.reset_mock()
        mock_exch.refresh.side_effect = None

        cl.connect(mock_exch)
        mock_exch.connect.assert_called_once()
        assert is_connected(cl, mock_exch)


def test_connect_when_reconnecting_error():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = False
        cl.connect(mock_exch)
        mock_exch.refresh.side_effect = AMQPConnectionError
        cl.refresh_pools()
        assert is_reconnecting(cl, mock_exch)
        mock_exch.connect.reset_mock()

        mock_exch.connect.side_effect = AMQPConnectionError
        cl.connect(mock_exch)
        mock_exch.connect.assert_called()
        assert is_reconnecting(cl, mock_exch)


def test_disconnect_one():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        cl.connect(mock_exch)
        cl.disconnect(exchange=mock_exch)
        mock_exch.close.assert_called_once()
        assert is_disconnected(cl, mock_exch)


def test_disconnect_all():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange"):
        mock_exch1 = mock.Mock(wraps=mq.AmqpExchange)
        mock_exch2 = mock.Mock(wraps=mq.AmqpExchange)
        cl.connect(mock_exch1)
        cl.connect(mock_exch2)

        # make this exchange 'reconnect'
        mock_exch1.refresh.side_effect = AMQPConnectionError
        cl.refresh_pools()

        cl.disconnect()
        mock_exch1.close.assert_called_once()
        mock_exch2.close.assert_called_once()
        assert is_disconnected(cl, mock_exch2)
        assert is_disconnected(cl, mock_exch1)
        assert cl.connections == {}


def test_refresh_to_reconnect():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = False
        cl.connect(mock_exch)
        assert is_connected(cl, mock_exch)
        mock_exch.refresh.reset_mock()

        mock_exch.refresh.side_effect = AMQPConnectionError
        cl.refresh_pools()
        mock_exch.refresh.assert_called_once()
        assert is_reconnecting(cl, mock_exch)


def test_refresh_to_connect():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        mock_exch.connected = False
        cl.connect(mock_exch)
        assert is_connected(cl, mock_exch)
        mock_exch.refresh.side_effect = AMQPConnectionError
        cl.refresh_pools()
        assert is_reconnecting(cl, mock_exch)

        mock_exch.connect.return_value = NOTYET
        cl.refresh_pools()
        assert is_reconnecting(cl, mock_exch)

        mock_exch.refresh.side_effect = None
        mock_exch.connect.return_value = None
        cl.refresh_pools()
        assert is_connected(cl, mock_exch)


def test_publish_no_connections():
    cl = mq.AmqpClient()
    assert cl.publish("hi") == {}


def test_publish_success():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        cl.connect(mock_exch)
        assert is_connected(cl, mock_exch)

        mock_exch.produce.return_value = True

        status = cl.publish("hi")
        assert status[mock_exch.identifier] == mq.DeliveryStatus.DELIVERED


def test_publish_nack():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        cl.connect(mock_exch)
        assert is_connected(cl, mock_exch)

        mock_exch.produce.return_value = False

        status = cl.publish("hi")
        assert status[mock_exch.identifier] == mq.DeliveryStatus.REJECTED


def test_publish_error():
    cl = mq.AmqpClient()
    with mock.patch("ssec_amqp.AmqpExchange") as mock_exch:
        cl.connect(mock_exch)
        assert is_connected(cl, mock_exch)

        mock_exch.produce.side_effect = AMQPConnectionError
        mock_exch.connect.side_effect = AMQPConnectionError

        status = cl.publish("hi")
        assert status[mock_exch.identifier] == mq.DeliveryStatus.DROPPED
        assert is_reconnecting(cl, mock_exch)
