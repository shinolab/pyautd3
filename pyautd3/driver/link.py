from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi_driver import LinkBuilderPtr, LinkPtr

__all__ = []  # type: ignore[var-annotated]

L = TypeVar("L", bound="Link")


class Link(metaclass=ABCMeta):
    _ptr: LinkPtr

    def __init__(self: Self, ptr: LinkPtr) -> None:
        self._ptr = ptr


class LinkBuilder(Generic[L], metaclass=ABCMeta):
    @abstractmethod
    def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
        pass

    @abstractmethod
    def _resolve_link(self: Self, _ptr: ControllerPtr) -> L:
        pass
