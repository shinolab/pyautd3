from pyautd3.link.remote import Remote, RemoteOption


def test_remote():
    _ = Remote("127.0.0.1:8080", RemoteOption())
