from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _validate_ptr


class TwinCAT(Link):
    def __init__(self: Self) -> None:
        super().__init__()

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkTwinCAT().link_twin_cat())  # pragma: no cover
