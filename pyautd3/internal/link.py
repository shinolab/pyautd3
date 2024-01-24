from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.native_methods.autd3capi_def import ControllerPtr, LinkBuilderPtr, LinkPtr

__all__ = []  # type: ignore[var-annotated]

L = TypeVar("L", bound="Link")


class Link(metaclass=ABCMeta):
    _ptr: LinkPtr

    def __init__(self: "Link", ptr: LinkPtr) -> None:
        self._ptr = ptr


class LinkBuilder(Generic[L], metaclass=ABCMeta):
    @abstractmethod
    def _link_builder_ptr(self: "LinkBuilder") -> LinkBuilderPtr:
        pass

    @abstractmethod
    def _resolve_link(self: "LinkBuilder", _ptr: ControllerPtr) -> L:
        pass
