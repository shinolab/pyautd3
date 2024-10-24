from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import (
    NativeMethods as Base,
)
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _validate_ptr


class TwinCAT(Link):
    class _Builder(LinkBuilder["TwinCAT"]):
        def _resolve_link(self: "TwinCAT._Builder", handle: HandlePtr, ptr: ControllerPtr) -> "TwinCAT":
            return TwinCAT(handle, Base().link_get(ptr))  # pragma: no cover

        def _link_builder_ptr(self: LinkBuilder) -> LinkBuilderPtr:
            return LinkTwinCAT().link_twin_cat()

    def __init__(self: "TwinCAT", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder() -> _Builder:
        return TwinCAT._Builder()


class RemoteTwinCAT(Link):
    class _Builder(LinkBuilder["RemoteTwinCAT"]):
        server_ams_net_id: str
        server_ip: str
        client_ams_net_id: str

        def __init__(self: "RemoteTwinCAT._Builder", server_ams_net_id: str) -> None:
            self.server_ams_net_id = server_ams_net_id
            self.server_ip = ""
            self.client_ams_net_id = ""

        def with_server_ip(self: "RemoteTwinCAT._Builder", ip: str) -> "RemoteTwinCAT._Builder":
            self.server_ip = ip
            return self

        def with_client_ams_net_id(self: "RemoteTwinCAT._Builder", ams_net_id: str) -> "RemoteTwinCAT._Builder":
            self.client_ams_net_id = ams_net_id
            return self

        def _link_builder_ptr(self: "RemoteTwinCAT._Builder") -> LinkBuilderPtr:
            return _validate_ptr(
                LinkTwinCAT().link_remote_twin_cat(
                    self.server_ams_net_id.encode("utf-8"),
                    self.server_ip.encode("utf-8"),
                    self.client_ams_net_id.encode("utf-8"),
                ),
            )

        def _resolve_link(self: "RemoteTwinCAT._Builder", handle: HandlePtr, _ptr: ControllerPtr) -> "RemoteTwinCAT":
            return RemoteTwinCAT(handle, Base().link_get(_ptr))  # pragma: no cover

    def __init__(self: "RemoteTwinCAT", handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(server_ams_net_id: str) -> _Builder:
        return RemoteTwinCAT._Builder(server_ams_net_id)
