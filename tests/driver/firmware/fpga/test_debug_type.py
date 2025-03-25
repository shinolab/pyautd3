import pytest

from pyautd3.driver.datagram.debug import GPIOOutputType


def test_debug_type_ctor():
    with pytest.raises(NotImplementedError):
        _ = GPIOOutputType()
