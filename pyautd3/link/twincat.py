from typing import Self

from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class _TwinCATBuilder(LinkBuilder["TwinCAT"]):
    def _resolve_link(self: Self, ptr: ControllerPtr) -> "TwinCAT":
        return TwinCAT(Base().link_get(ptr))  # pragma: no cover

    def _link_builder_ptr(self: LinkBuilder) -> LinkBuilderPtr:
        return LinkTwinCAT().link_twin_cat()  # pragma: no cover


class TwinCAT(Link):
    @staticmethod
    def builder() -> _TwinCATBuilder:
        return _TwinCATBuilder()

    def __init__(self: Self, ptr: LinkPtr) -> None:
        super().__init__(ptr)  # pragma: no cover


class RemoteTwinCATOption:
    server_ip: str
    client_ams_net_id: str

    def __init__(self: Self, *, server_ip: str = "", client_ams_net_id: str = "") -> None:
        self.server_ip = server_ip
        self.client_ams_net_id = client_ams_net_id


class _RemoteTwinCATBuilder(LinkBuilder["RemoteTwinCAT"]):
    server_ams_net_id: str
    option: RemoteTwinCATOption

    def __init__(self: Self, server_ams_net_id: str, option: RemoteTwinCATOption) -> None:
        self.server_ams_net_id = server_ams_net_id
        self.option = option

    def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
        return _validate_ptr(  # pragma: no cover
            LinkTwinCAT().link_remote_twin_cat(
                _to_null_terminated_utf8(self.server_ams_net_id),
                _to_null_terminated_utf8(self.option.server_ip),
                _to_null_terminated_utf8(self.option.client_ams_net_id),
            ),
        )

    def _resolve_link(self: Self, _ptr: ControllerPtr) -> "RemoteTwinCAT":
        return RemoteTwinCAT(Base().link_get(_ptr))  # pragma: no cover


class RemoteTwinCAT(Link):
    def __init__(self: Self, ptr: LinkPtr) -> None:
        super().__init__(ptr)  # pragma: no cover

    @staticmethod
    def builder(*, server_ams_net_id: str, option: RemoteTwinCATOption) -> _RemoteTwinCATBuilder:
        return _RemoteTwinCATBuilder(server_ams_net_id, option)
