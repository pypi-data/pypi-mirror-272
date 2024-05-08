import json
from typing import Hashable
from unittest import mock

import pytest
from amqp.exceptions import ConnectionForced, MessageNacked, RecoverableConnectionError
from ssec_amqp import (
    AmqpExchange,
)
from ssec_amqp._defs import (
    DEFAULT_EXCHANGE,
    DEFAULT_PORT,
    DEFAULT_VHOST,
    DEFUALT_ROUTE_KEY,
    AMQPConnectionError,
    StateError,
)


def test_initialization():
    test_dest = "amqp"
    test_user = "u"
    test_pass = "p"
    test_port = 123
    test_vhost = "/new"
    test_exch = "model"

    ex = AmqpExchange(test_dest, test_user, test_pass)

    assert not ex.connected
    assert ex.host == test_dest
    assert ex.user == test_user
    assert ex.port == DEFAULT_PORT
    assert ex.exchange == DEFAULT_EXCHANGE
    assert ex.vhost == DEFAULT_VHOST

    ex1 = AmqpExchange(test_dest, test_user, test_pass, test_exch, test_vhost, test_port)

    assert ex1.port == test_port
    assert ex1.vhost == test_vhost
    assert ex1.exchange == test_exch


def test_connect_error():
    ex = AmqpExchange("localhost", "guest", "guest")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        mock_con.connected = False
        mock_con.connect.side_effect = RecoverableConnectionError
        with pytest.raises(AMQPConnectionError):
            ex.connect()


def test_connect():
    ex = AmqpExchange("localhost", "guest", "guest")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        mock_con.connected = False
        ex.connect()
        mock_con.connect.assert_called_once()
        mock_con.channel.assert_called_once()
        mock_con.connected = True
        ex.connect()
        mock_con.connect.assert_called_once()
        mock_con.channel.assert_called_once()


@pytest.mark.parametrize(
    ("con1", "con2"),
    [
        (("host",), ("host",)),
        (("host1",), ("host2",)),
        (("host", "user"), ("host", "user")),
        (
            (
                "host",
                "user1",
            ),
            ("host", "user2"),
        ),
        (("host", "user", "pass"), ("host", "user", "pass")),
        (("host", "user", "pass1"), ("host", "user", "pass2")),
        (("host", "user", "pass", "exch"), ("host", "user", "pass", "exch")),
        (("host", "user", "pass", "exch1"), ("host", "user", "pass", "exch2")),
        (
            ("host", "user", "pass", "exch", "vhost"),
            ("host", "user", "pass", "exch", "vhost"),
        ),
        (
            ("host", "user", "pass", "exch", "vhost1"),
            ("host", "user", "pass", "exch", "vhost2"),
        ),
        (
            ("host", "user", "pass", "exch", "vhost", 4000),
            ("host", "user", "pass", "exch", "vhost", 4000),
        ),
        (
            ("host", "user", "pass", "exch", "vhost", 4001),
            ("host", "user", "pass", "exch", "vhost", 4002),
        ),
    ],
)
def test_equality(con1, con2):
    ex1 = AmqpExchange(*con1)
    ex2 = AmqpExchange(*con2)
    assert ex1 != con1
    assert ex2 != con2
    if con1 == con2:
        assert ex1 == ex2
        assert ex1.identifier == ex2.identifier
    elif con1[:2] == con2[:2] and con1[3:] == con2[3:]:
        # password doesn't get checked for equality!
        assert ex1 == ex2
        assert ex1.identifier == ex2.identifier
    else:
        assert ex1 != ex2
        assert ex1.identifier != ex2.identifier


def test_hashable():
    assert isinstance(AmqpExchange, Hashable)
    ex1 = AmqpExchange("test")
    ex2 = AmqpExchange("test")
    ex3 = AmqpExchange("nottest")
    assert hash(ex1) == hash(ex2)
    assert hash(ex2) != hash(ex3)


def test_refresh_not_connected():
    ex = AmqpExchange("test")
    with pytest.raises(StateError):
        ex.refresh()


def test_refresh():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        mock_con.connected = False
        ex.refresh()
        mock_con.heartbeat_tick.assert_called_once()


def test_refresh_error():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con, mock.patch.object(ex, "connect") as mock_method:
        mock_con.heartbeat_tick.side_effect = ConnectionForced
        ex.refresh()
        mock_method.assert_called_once()


def test_produce_not_connected():
    ex = AmqpExchange("test")
    with pytest.raises(StateError):
        ex.produce("hello")


def test_produce_nacked():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        ex.connect()
        mock_con.connected = True
        with mock.patch.object(ex, "_AmqpExchange__chan") as mock_chan:
            mock_chan.basic_publish.side_effect = MessageNacked
            assert not ex.produce("t")


def test_produce():
    ex = AmqpExchange("test")
    msg = {"test": "test"}
    msg_s = json.dumps(msg)
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        ex.connect()
        mock_con.connected = True
        with mock.patch.object(ex, "_AmqpExchange__chan") as mock_chan:
            assert ex.produce(msg)
            mock_chan.basic_publish.assert_called_once()
            kwargs = mock_chan.basic_publish.call_args.kwargs
            assert kwargs["msg"].body == msg_s
            assert kwargs["msg"].content_type == "application/json"
            assert kwargs["msg"].content_encoding == "utf-8"
            assert kwargs["exchange"] == ex.exchange
            assert kwargs["routing_key"] == DEFUALT_ROUTE_KEY


def test_produce_chan_reconnect():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn", create=True) as mock_con:
        # set up ex.__chan
        mock_con.connected = False
        ex.connect()
        mock_con.connected = True
        mock_con.reset_mock()
        with mock.patch.object(ex, "_channel_open") as mock_meth:
            mock_meth.return_value = False
            assert ex.produce("t")
            mock_con.channel.assert_called_once()


def test_close_not_connected():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        mock_con.connected = False
        ex.close()
        mock_con.collect.assert_called_once()


def test_close():
    ex = AmqpExchange("test")
    with mock.patch.object(ex, "_AmqpExchange__conn") as mock_con:
        mock_con.connected = True

        ex.close()
        mock_con.collect.assert_called_once()
