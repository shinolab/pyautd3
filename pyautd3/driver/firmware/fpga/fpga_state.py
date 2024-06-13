from pyautd3.native_methods.autd3capi_driver import Segment


class FPGAState:
    _state: int

    def __init__(self: "FPGAState", info: int) -> None:
        self._state = info

    @property
    def is_thermal_assert(self: "FPGAState") -> bool:
        return (self._state & (1 << 0)) != 0

    @property
    def current_mod_segment(self: "FPGAState") -> Segment:
        match int(self._state) & (1 << 1):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def current_stm_segment(self: "FPGAState") -> Segment | None:
        if not self.is_stm_mode:
            return None

        match int(self._state) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def current_gain_segment(self: "FPGAState") -> Segment | None:
        if not self.is_gain_mode:
            return None

        match int(self._state) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    @property
    def is_gain_mode(self: "FPGAState") -> bool:
        return (int(self._state) & (1 << 3)) != 0

    @property
    def is_stm_mode(self: "FPGAState") -> bool:
        return not self.is_gain_mode
