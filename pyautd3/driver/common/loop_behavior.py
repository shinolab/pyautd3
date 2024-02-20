from pyautd3.autd_error import CantBeZeroError
from pyautd3.native_methods.autd3capi_def import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.autd3capi_def import NativeMethods as Def


class LoopBehavior:
    """Loop behavior."""

    _internal: _LoopBehavior

    def __new__(cls: type["LoopBehavior"]) -> "LoopBehavior":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["LoopBehavior"], internal: _LoopBehavior) -> "LoopBehavior":
        ins = super().__new__(cls)
        ins._internal = internal
        return ins

    @staticmethod
    def infinite() -> "LoopBehavior":
        """Infinite."""
        return LoopBehavior.__private_new__(Def().loop_behavior_infinite())

    @staticmethod
    def finite(v: int) -> "LoopBehavior":
        """Finite."""
        if v < 1:
            raise CantBeZeroError(v)
        return LoopBehavior.__private_new__(Def().loop_behavior_finite(v))

    @staticmethod
    def once() -> "LoopBehavior":
        """Equivalent to `finite(1)`."""
        return LoopBehavior.__private_new__(Def().loop_behavior_once())

    def __eq__(self: "LoopBehavior", value: object) -> bool:
        if not isinstance(value, LoopBehavior):
            return False
        return self._internal.rep == value._internal.rep
