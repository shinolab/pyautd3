import pytest

from pyautd3 import Drive, EmitIntensity, Phase


def test_drive():
    d = Drive((EmitIntensity(0x01), Phase(0x02)))
    assert d.intensity == EmitIntensity(0x01)
    assert d.phase == Phase(0x02)

    d = Drive((Phase(0x01), EmitIntensity(0x02)))
    assert d.intensity == EmitIntensity(0x02)
    assert d.phase == Phase(0x01)

    d = Drive(d)
    assert d.intensity == EmitIntensity(0x02)
    assert d.phase == Phase(0x01)

    d = Drive(EmitIntensity(0x01))
    assert d.intensity == EmitIntensity(0x01)
    assert d.phase == Phase(0x00)

    d = Drive(Phase(0x01))
    assert d.intensity == EmitIntensity(0xFF)
    assert d.phase == Phase(0x01)

    with pytest.raises(TypeError):
        _ = Drive((1, 2, 3))

    with pytest.raises(TypeError):
        _ = Drive((1, 2))

    with pytest.raises(TypeError):
        _ = Drive(1)  # type: ignore[arg-type]
