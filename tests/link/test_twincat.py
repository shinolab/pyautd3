from pyautd3.link.twincat import RemoteTwinCAT, RemoteTwinCATOption, TwinCAT


def test_twincat():
    _ = TwinCAT.builder()


def test_remote_twincat():
    _ = RemoteTwinCAT.builder(
        server_ams_net_id="xxx.xxx.xxx.xxx.xxx.xxx",
        option=RemoteTwinCATOption(server_ip="127.0.0.1", client_ams_net_id="127.0.0.1"),
    )
