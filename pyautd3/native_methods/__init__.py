import contextlib
import os
import os.path
import platform
import sys
from pathlib import Path

from .autd3capi import NativeMethods as Base
from .autd3capi_gain_holo import NativeMethods as GainHolo
from .autd3capi_link_simulator import NativeMethods as LinkSimulator
from .autd3capi_link_twincat import NativeMethods as LinkTwincAT
from .autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile

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
    err = "Not supported OS"
    raise ImportError(err)

_LIB_PATH = Path(__file__).parent.parent / "bin"

Base().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
GainHolo().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
ModulationAudioFile().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
LinkSimulator().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
if sys.platform == "win32":
    with contextlib.suppress(FileNotFoundError):
        os.add_dll_directory("C:\\TwinCAT\\Common64")
with contextlib.suppress(Exception):
    LinkTwincAT().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)
