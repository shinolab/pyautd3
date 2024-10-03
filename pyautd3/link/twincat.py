from datetime import timedelta

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import LinkRemoteTwinCATBuilderPtr, LinkTwinCATBuilderPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _validate_ptr


class TwinCAT(Link):
    class _Builder(LinkBuilder["TwinCAT"]):
        _builder: LinkTwinCATBuilderPtr

        def __init__(self: "TwinCAT._Builder") -> None:
            self._builder = LinkTwinCAT().link_twin_cat()

        def with_timeout(self: "TwinCAT._Builder", timeout: timedelta) -> "TwinCAT._Builder":
            self._builder = LinkTwinCAT().link_twin_cat_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "TwinCAT._Builder") -> LinkBuilderPtr:
            return LinkTwinCAT().link_twin_cat_into_builder(self._builder)  # pragma: no cover

        def _resolve_link(self: "TwinCAT._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "TwinCAT":
            return TwinCAT(handle, Base().link_get(ptr))  # pragma: no cover

    def __init__(self: "TwinCAT", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder() -> _Builder:
        return TwinCAT._Builder()


class RemoteTwinCAT(Link):
    class _Builder(LinkBuilder["RemoteTwinCAT"]):
        _builder: LinkRemoteTwinCATBuilderPtr

        def __init__(self: "RemoteTwinCAT._Builder", server_ams_net_id: str) -> None:
            self._builder = _validate_ptr(LinkTwinCAT().link_remote_twin_cat(server_ams_net_id.encode("utf-8")))

        def with_server_ip(self: "RemoteTwinCAT._Builder", ip: str) -> "RemoteTwinCAT._Builder":
            self._builder = LinkTwinCAT().link_remote_twin_cat_with_server_ip(self._builder, ip.encode("utf-8"))
            return self

        def with_client_ams_net_id(self: "RemoteTwinCAT._Builder", ams_net_id: str) -> "RemoteTwinCAT._Builder":
            self._builder = LinkTwinCAT().link_remote_twin_cat_with_client_ams_net_id(self._builder, ams_net_id.encode("utf-8"))
            return self

        def with_timeout(self: "RemoteTwinCAT._Builder", timeout: timedelta) -> "RemoteTwinCAT._Builder":
            self._builder = LinkTwinCAT().link_remote_twin_cat_with_timeout(self._builder, int(timeout.total_seconds() * 1000 * 1000 * 1000))
            return self

        def _link_builder_ptr(self: "RemoteTwinCAT._Builder") -> LinkBuilderPtr:
            return LinkTwinCAT().link_remote_twin_cat_into_builder(self._builder)  # pragma: no cover

        def _resolve_link(self: "RemoteTwinCAT._Builder", handle: HandlePtr, _ptr: ControllerPtr) -> "RemoteTwinCAT":
            return RemoteTwinCAT(handle, Base().link_get(_ptr))  # pragma: no cover

    def __init__(self: "RemoteTwinCAT", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(server_ams_net_id: str) -> _Builder:
        return RemoteTwinCAT._Builder(server_ams_net_id)
