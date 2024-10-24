from pyautd3.link.twincat import RemoteTwinCAT, TwinCAT


def test_twincat():
    _ = TwinCAT.builder()


def test_remote_twincat():
    _ = RemoteTwinCAT.builder("xxx.xxx.xxx.xxx.xxx.xxx").with_server_ip("127.0.0.1").with_client_ams_net_id("127.0.0.1")
