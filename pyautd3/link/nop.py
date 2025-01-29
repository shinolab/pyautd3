from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi import NativeMethods as LinkNop
from pyautd3.native_methods.autd3capi_driver import LinkPtr


class Nop(Link):
    def __init__(self: Self) -> None:
        super().__init__()

    def _resolve(self: Self) -> LinkPtr:
        return LinkNop().link_nop()
