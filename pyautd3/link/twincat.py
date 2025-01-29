from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.autd3capi_link_twincat import NativeMethods as LinkTwinCAT
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class TwinCAT(Link):
    def __init__(self: Self) -> None:
        super().__init__()

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkTwinCAT().link_twin_cat())  # pragma: no cover


class RemoteTwinCATOption:
    server_ip: str
    client_ams_net_id: str

    def __init__(self: Self, *, server_ip: str = "", client_ams_net_id: str = "") -> None:
        self.server_ip = server_ip
        self.client_ams_net_id = client_ams_net_id


class RemoteTwinCAT(Link):
    server_ams_net_id: str
    option: RemoteTwinCATOption

    def __init__(self: Self, server_ams_net_id: str, option: RemoteTwinCATOption) -> None:
        super().__init__()
        self.server_ams_net_id = server_ams_net_id
        self.option = option

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(  # pragma: no cover
            LinkTwinCAT().link_remote_twin_cat(
                _to_null_terminated_utf8(self.server_ams_net_id),
                _to_null_terminated_utf8(self.option.server_ip),
                _to_null_terminated_utf8(self.option.client_ams_net_id),
            ),
        )
