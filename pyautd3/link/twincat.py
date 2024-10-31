from typing import Self

from pyautd3.derive import builder
from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class _TwinCATBuilder(LinkBuilder["TwinCAT"]):
    def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "TwinCAT":
        return TwinCAT(handle, Base().link_get(ptr))  # pragma: no cover

    def _link_builder_ptr(self: LinkBuilder) -> LinkBuilderPtr:
        return LinkTwinCAT().link_twin_cat()  # pragma: no cover


class TwinCAT(Link):
    @staticmethod
    def builder() -> _TwinCATBuilder:
        return _TwinCATBuilder()

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover


@builder
class _RemoteTwinCATBuilder(LinkBuilder["RemoteTwinCAT"]):
    _prop_server_ams_net_id: str
    _param_server_ip: str
    _param_client_ams_net_id: str

    def __init__(self: Self, server_ams_net_id: str) -> None:
        self._prop_server_ams_net_id = server_ams_net_id
        self._param_server_ip = ""
        self._param_client_ams_net_id = ""

    def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
        return _validate_ptr(  # pragma: no cover
            LinkTwinCAT().link_remote_twin_cat(
                _to_null_terminated_utf8(self._prop_server_ams_net_id),
                _to_null_terminated_utf8(self._param_server_ip),
                _to_null_terminated_utf8(self._param_client_ams_net_id),
            ),
        )

    def _resolve_link(self: Self, handle: HandlePtr, _ptr: ControllerPtr) -> "RemoteTwinCAT":
        return RemoteTwinCAT(handle, Base().link_get(_ptr))  # pragma: no cover


class RemoteTwinCAT(Link):
    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr) -> None:
        super().__init__(handle, ptr)  # pragma: no cover

    @staticmethod
    def builder(server_ams_net_id: str) -> _RemoteTwinCATBuilder:
        return _RemoteTwinCATBuilder(server_ams_net_id)
