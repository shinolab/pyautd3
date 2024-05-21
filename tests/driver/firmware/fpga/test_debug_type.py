import pytest

from pyautd3.driver.datagram.debug import DebugType


def test_debug_type_ctor():
    with pytest.raises(NotImplementedError):
        _ = DebugType()
