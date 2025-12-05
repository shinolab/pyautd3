import pytest

from pyautd3.driver.utils import _validate_nonzero_u16, _validate_nonzero_u32


def test_validate_nonzero_u16():
    assert _validate_nonzero_u16(1) == 1
    assert _validate_nonzero_u16(0xFFFF) == 0xFFFF

    with pytest.raises(TypeError):
        _ = _validate_nonzero_u16(0.1)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u16(0)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u16(0xFFFF + 1)


def test_validate_nonzero_u32():
    assert _validate_nonzero_u32(1) == 1
    assert _validate_nonzero_u32(0xFFFFFFFF) == 0xFFFFFFFF

    with pytest.raises(TypeError):
        _ = _validate_nonzero_u32(0.1)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u32(0)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u32(0xFFFFFFFF + 1)
