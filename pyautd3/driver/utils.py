def _validate_u8(value: int) -> int:
    if isinstance(value, float):
        raise TypeError
    if value < 0 or value > 0xFF:  # noqa: PLR2004
        raise ValueError
    return value
