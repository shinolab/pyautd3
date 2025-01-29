from pyautd3.link.twincat import RemoteTwinCAT, RemoteTwinCATOption, TwinCAT


def test_twincat():
    _ = TwinCAT()


def test_remote_twincat():
    _ = RemoteTwinCAT(
        "xxx.xxx.xxx.xxx.xxx.xxx",
        RemoteTwinCATOption(server_ip="127.0.0.1", client_ams_net_id="127.0.0.1"),
    )
