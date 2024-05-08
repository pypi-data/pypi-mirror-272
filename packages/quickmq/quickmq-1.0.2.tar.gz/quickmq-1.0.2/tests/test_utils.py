from __future__ import annotations

from typing import Any

import pytest
from amqp.exceptions import RecoverableConnectionError
from ssec_amqp._utils import AMQPConnectionError, catch_amqp_errors


def mock_function(to_return: Any | None = None, to_raise: Exception | None = None):
    if to_return is not None:
        return to_return
    if to_raise is not None:
        raise to_raise
    return None


def test_catch_amqp_errors_no_error():
    rv = 5
    assert catch_amqp_errors(mock_function)(to_return=rv) == rv


def test_catch_amqp_errors_amqp_error():
    with pytest.raises(AMQPConnectionError):
        catch_amqp_errors(mock_function)(to_raise=RecoverableConnectionError)


def test_catch_amqp_errors_diff_error():
    err = TypeError
    with pytest.raises(err):
        catch_amqp_errors(mock_function)(to_raise=err)
