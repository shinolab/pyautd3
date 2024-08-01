import pytest

from pyautd3.driver.utils import _validate_nonzero_u16


def test_validate_nonzero_u16():
    assert _validate_nonzero_u16(1) == 1
    assert _validate_nonzero_u16(0xFFFF) == 0xFFFF

    with pytest.raises(TypeError):
        _ = _validate_nonzero_u16(0.1)  # type: ignore[arg-type]

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u16(0)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = _validate_nonzero_u16(0xFFFF + 1)
