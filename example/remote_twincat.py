import asyncio

from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.twincat import RemoteTwinCAT


async def main() -> None:
    remote_ip_addr = "remote ip addr"
    remore_ams_net_id = "remote ams net id"
    local_ams_net_id = "local ams net is"

    with await (
        Controller.builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .open_with_async(RemoteTwinCAT.builder(remore_ams_net_id).with_server_ip(remote_ip_addr).with_client_ams_net_id(local_ams_net_id))
    ) as autd:  # type: Controller
        await runner.run(autd)


if __name__ == "__main__":
    asyncio.run(main())
