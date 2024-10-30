from typing import Self

from pyautd3.derive import datagram, gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


@gain
@datagram
@datagram_with_segment
class Null(Gain):
    def __init__(self: Self) -> None:
        super().__init__()

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_null()
