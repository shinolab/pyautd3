from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

from pyautd3.native_methods.autd3capi_driver import LinkPtr

L = TypeVar("L", bound="Link")


class Link(metaclass=ABCMeta):
    _ptr: LinkPtr

    def __init__(self: Self) -> None:
        self._ptr = LinkPtr()

    @abstractmethod
    def _resolve(self: Self) -> LinkPtr:
        pass
