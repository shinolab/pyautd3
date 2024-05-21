import ctypes

from pyautd3.native_methods.autd3capi_driver import Segment


class FPGAState:
    info: ctypes.c_uint8

    def __init__(self: "FPGAState", info: ctypes.c_uint8) -> None:
        self.info = info

    @property
    def is_thermal_assert(self: "FPGAState") -> bool:
        return (int(self.info) & (1 << 0)) != 0

    @property
    def current_mod_segment(self: "FPGAState") -> Segment:
        match int(self.info) & (1 << 1):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def current_stm_segment(self: "FPGAState") -> Segment | None:
        if not self.is_stm_mode:
            return None

        match int(self.info) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def current_gain_segment(self: "FPGAState") -> Segment | None:
        if not self.is_gain_mode:
            return None

        match int(self.info) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def is_gain_mode(self: "FPGAState") -> bool:
        return (int(self.info) & (1 << 3)) != 0

    @property
    def is_stm_mode(self: "FPGAState") -> bool:
        return not self.is_gain_mode
