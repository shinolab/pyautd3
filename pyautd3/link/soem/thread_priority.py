from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3.native_methods.autd3capi_link_soem import ThreadPriorityPtr
from pyautd3.native_methods.utils import ConstantADT


class ThreadPriority(metaclass=ConstantADT):
    Min: ThreadPriorityPtr = LinkSOEM().link_soem_thread_priority_min()
    Max: ThreadPriorityPtr = LinkSOEM().link_soem_thread_priority_max()

    @staticmethod
    def Crossplatform(value: int) -> ThreadPriorityPtr:  # noqa: N802
        if not (0 <= value <= 99):  # noqa: PLR2004
            msg = "value must be between 0 and 99"
            raise ValueError(msg)
        return LinkSOEM().link_soem_thread_priority_crossplatform(value)
