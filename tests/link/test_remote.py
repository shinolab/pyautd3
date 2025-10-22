from pyautd3 import Duration
from pyautd3.link.remote import Remote, RemoteOption


def test_option():
    option = RemoteOption()
    inner = option._inner()
    assert not inner.timeout.has_value

    option = RemoteOption(timeout=Duration.from_nanos(0))
    inner = option._inner()
    assert inner.timeout.has_value
    assert inner.timeout.value == Duration.from_nanos(0)._inner


def test_remote():
    _ = Remote("127.0.0.1:8080", RemoteOption())
