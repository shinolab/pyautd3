import pytest

from pyautd3.utils import Duration


def test_duration():
    d = Duration.from_nanos(1)
    assert d.as_nanos() == 1

    d = Duration.from_micros(1)
    assert d.as_nanos() == 1000
    assert d.as_micros() == 1

    d = Duration.from_millis(1)
    assert d.as_nanos() == 1000000
    assert d.as_micros() == 1000
    assert d.as_millis() == 1

    d = Duration.from_secs(1)
    assert d.as_nanos() == 1000000000
    assert d.as_micros() == 1000000
    assert d.as_millis() == 1000
    assert d.as_secs() == 1

    d1 = Duration.from_micros(1)
    d2 = Duration.from_micros(2)
    assert (d1 + d2).as_micros() == 3
    assert (d2 - d1).as_micros() == 1
    assert (d1 * 2).as_micros() == 2
    assert (d2 / 2).as_micros() == 1
    assert (d1 / 2).as_nanos() == 500
    assert (d1 // 2).as_nanos() == 500
    assert (d1 % 300).as_nanos() == 100
    assert divmod(d1, 300) == (3, Duration.from_nanos(100))
    assert not (d1 == 1000)  # noqa: SIM201
    assert d1 != 1000
    assert d1 == Duration.from_nanos(1000)
    assert d1 != d2
    assert d1 < d2
    assert d1 <= d2
    assert d2 > d1
    assert d2 >= d1
    assert hash(d1) == hash(1000)
    assert str(Duration.from_nanos(1)) == "1ns"
    assert str(Duration.from_nanos(1001)) == "1.001μs"
    assert str(Duration.from_nanos(1100)) == "1.1μs"
    assert str(Duration.from_micros(1)) == "1μs"
    assert str(Duration.from_micros(1001)) == "1.001ms"
    assert str(Duration.from_micros(1100)) == "1.1ms"
    assert str(Duration.from_millis(1)) == "1ms"
    assert str(Duration.from_millis(1001)) == "1.001s"
    assert str(Duration.from_millis(1100)) == "1.1s"
    assert str(Duration.from_secs(1)) == "1s"

    with pytest.raises(NotImplementedError):
        _ = Duration()
