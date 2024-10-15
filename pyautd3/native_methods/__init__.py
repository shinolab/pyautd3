import ctypes
import os
import os.path
import platform
import sys

from .autd3capi import NativeMethods as Base
from .autd3capi_gain_holo import NativeMethods as GainHolo
from .autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from .autd3capi_link_simulator import NativeMethods as LinkSimulator
from .autd3capi_link_twincat import NativeMethods as LinkTwincAT
from .autd3capi_link_soem import NativeMethods as LinkSOEM, ThreadPriorityPtr
from .autd3capi_emulator import NativeMethods as Emulator

_PLATFORM = platform.system()
_PREFIX = ""
_BIN_EXT = ""
if _PLATFORM == "Windows":
    _BIN_EXT = ".dll"
elif _PLATFORM == "Darwin":
    _PREFIX = "lib"
    _BIN_EXT = ".dylib"
elif _PLATFORM == "Linux":
    _PREFIX = "lib"
    _BIN_EXT = ".so"
else:
    raise ImportError("Not supported OS")

_LIB_PATH = os.path.join(os.path.dirname(__file__), "..", "bin")

Base().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
GainHolo().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
ModulationAudioFile().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
LinkSimulator().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
try:
    LinkSOEM().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
except Exception:                                                                    # pragma: no cover
    def _dummy() -> ThreadPriorityPtr:                                               # pragma: no cover
        return ThreadPriorityPtr(ctypes.c_void_p())                                  # pragma: no cover
    LinkSOEM().link_soem_thread_priority_min = _dummy  # type: ignore[method-assign] # pragma: no cover
    LinkSOEM().link_soem_thread_priority_max = _dummy  # type: ignore[method-assign] # pragma: no cover
if sys.platform == "win32":
    try:
        os.add_dll_directory("C:\\TwinCAT\\Common64")
    except FileNotFoundError:
        pass
try:
    LinkTwincAT().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
except Exception:   # pragma: no cover
    pass          # pragma: no cover
Emulator().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
