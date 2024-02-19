from pyautd3.driver.datagram.gain import IGain, IGainWithCache, IGainWithTransform
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GainPtr


class Null(IGainWithCache, IGainWithTransform, IGain):
    """Gain to output nothing."""

    def __init__(self: "Null") -> None:
        super().__init__()

    def _gain_ptr(self: "Null", _: Geometry) -> GainPtr:
        return Base().gain_null()
