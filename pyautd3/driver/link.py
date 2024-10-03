from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr

__all__ = []  # type: ignore[var-annotated]

L = TypeVar("L", bound="Link")


class Link(metaclass=ABCMeta):
    _ptr: LinkPtr
    _handle: HandlePtr

    def __init__(self: "Link", handle: HandlePtr, ptr: LinkPtr) -> None:
        self._ptr = ptr
        self._handle = handle


class LinkBuilder(Generic[L], metaclass=ABCMeta):
    @abstractmethod
    def _link_builder_ptr(self: "LinkBuilder") -> LinkBuilderPtr:
        pass

    @abstractmethod
    def _resolve_link(self: "LinkBuilder", _handle: HandlePtr, _ptr: ControllerPtr) -> L:
        pass
