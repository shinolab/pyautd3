import ctypes


class FPGAState:
    """FPGA information."""

    info: ctypes.c_uint8

    def __init__(self: "FPGAState", info: ctypes.c_uint8) -> None:
        self.info = info

    def is_thermal_assert(self: "FPGAState") -> bool:
        """Check if thermal sensor is asserted."""
        return (int(self.info) & 0x01) != 0

    def __str__(self: "FPGAState") -> str:
        return f"Thermal assert = {self.is_thermal_assert()}"
