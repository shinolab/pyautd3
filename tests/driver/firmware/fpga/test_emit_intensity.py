import pytest

from pyautd3 import Intensity


def test_emit_intensity():
    for i in range(256):
        intensity = Intensity(i)
        assert intensity.value == i
        assert str(intensity) == f"Intensity({i})"

    with pytest.raises(TypeError):
        _ = Intensity(0.0)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Intensity(-1)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Intensity(256)


def test_emit_intensity_min_max():
    assert Intensity.MIN.value == 0x00
    assert Intensity.MAX.value == 0xFF


def test_emit_intensity_floordiv():
    assert Intensity(0xFF) // 2 == Intensity(0x7F)
