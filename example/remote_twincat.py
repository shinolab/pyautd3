from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.twincat import RemoteTwinCAT, RemoteTwinCATOption

if __name__ == "__main__":
    with Controller.open(
        [AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])],
        RemoteTwinCAT(
            server_ams_net_id="remote ams net id",
            option=RemoteTwinCATOption(
                server_ip="server ip addr (optional)",
                client_ams_net_id="local ams net is (optional)",
            ),
        ),
    ) as autd:
        runner.run(autd)
