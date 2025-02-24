import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import ResultModulation, ResultStatus, SamplingConfigWrap


class Singleton(type):
    _instances = {}  # type: ignore[var-annotated]
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_modulation_audio_file{bin_ext}"))

        self.dll.AUTDModulationAudioFileTracingInit.argtypes = []
        self.dll.AUTDModulationAudioFileTracingInit.restype = None

        self.dll.AUTDModulationAudioFileTracingInitWithFile.argtypes = [ctypes.c_char_p]
        self.dll.AUTDModulationAudioFileTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDModulationAudioFileWav.argtypes = [ctypes.c_char_p]
        self.dll.AUTDModulationAudioFileWav.restype = ResultModulation

        self.dll.AUTDModulationAudioFileCsv.argtypes = [ctypes.c_char_p, SamplingConfigWrap, ctypes.c_uint8]
        self.dll.AUTDModulationAudioFileCsv.restype = ResultModulation

    def modulation_audio_file_tracing_init(self) -> None:
        return self.dll.AUTDModulationAudioFileTracingInit()

    def modulation_audio_file_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDModulationAudioFileTracingInitWithFile(path)

    def modulation_audio_file_wav(self, path: bytes) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileWav(path)

    def modulation_audio_file_csv(self, path: bytes, sampling_config: SamplingConfigWrap, delimiter: int) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileCsv(path, sampling_config, delimiter)
