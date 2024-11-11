# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Vector3, Quaternion, FfiFuture, LocalFfiFuture
from pyautd3.native_methods.autd3_driver import SamplingConfig, LoopBehavior, SyncMode, GainSTMMode, GPIOOut, GPIOIn, Segment, SilencerTarget, Drive, DcSysTime
from pyautd3.native_methods.autd3capi_driver import DynSincInterpolator, ResultModulation, ResultStatus



class Singleton(type):
    _instances = {}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_modulation_audio_file{bin_ext}'))

        self.dll.AUTDModulationAudioFileTracingInit.argtypes = [] 
        self.dll.AUTDModulationAudioFileTracingInit.restype = None

        self.dll.AUTDModulationAudioFileTracingInitWithFile.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDModulationAudioFileTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDModulationAudioFileWav.argtypes = [ctypes.c_char_p, LoopBehavior]  # type: ignore 
        self.dll.AUTDModulationAudioFileWav.restype = ResultModulation

        self.dll.AUTDModulationAudioFileWavWithResample.argtypes = [ctypes.c_char_p, LoopBehavior, SamplingConfig, DynSincInterpolator]  # type: ignore 
        self.dll.AUTDModulationAudioFileWavWithResample.restype = ResultModulation

        self.dll.AUTDModulationAudioFileRawPCM.argtypes = [ctypes.c_char_p, SamplingConfig, LoopBehavior]  # type: ignore 
        self.dll.AUTDModulationAudioFileRawPCM.restype = ResultModulation

        self.dll.AUTDModulationAudioFileRawPCMWithResample.argtypes = [ctypes.c_char_p, LoopBehavior, ctypes.c_float, SamplingConfig, DynSincInterpolator]  # type: ignore 
        self.dll.AUTDModulationAudioFileRawPCMWithResample.restype = ResultModulation

        self.dll.AUTDModulationAudioFileCsv.argtypes = [ctypes.c_char_p, SamplingConfig, ctypes.c_uint8, LoopBehavior]  # type: ignore 
        self.dll.AUTDModulationAudioFileCsv.restype = ResultModulation

        self.dll.AUTDModulationAudioFileCsvWithResample.argtypes = [ctypes.c_char_p, ctypes.c_uint8, LoopBehavior, ctypes.c_float, SamplingConfig, DynSincInterpolator]  # type: ignore 
        self.dll.AUTDModulationAudioFileCsvWithResample.restype = ResultModulation

    def modulation_audio_file_tracing_init(self) -> None:
        return self.dll.AUTDModulationAudioFileTracingInit()

    def modulation_audio_file_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDModulationAudioFileTracingInitWithFile(path)

    def modulation_audio_file_wav(self, path: bytes, loop_behavior: LoopBehavior) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileWav(path, loop_behavior)

    def modulation_audio_file_wav_with_resample(self, path: bytes, loop_behavior: LoopBehavior, target: SamplingConfig, resample: DynSincInterpolator) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileWavWithResample(path, loop_behavior, target, resample)

    def modulation_audio_file_raw_pcm(self, path: bytes, config: SamplingConfig, loop_behavior: LoopBehavior) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileRawPCM(path, config, loop_behavior)

    def modulation_audio_file_raw_pcm_with_resample(self, path: bytes, loop_behavior: LoopBehavior, src: float, target: SamplingConfig, resample: DynSincInterpolator) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileRawPCMWithResample(path, loop_behavior, src, target, resample)

    def modulation_audio_file_csv(self, path: bytes, config: SamplingConfig, deliminator: int, loop_behavior: LoopBehavior) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileCsv(path, config, deliminator, loop_behavior)

    def modulation_audio_file_csv_with_resample(self, path: bytes, deliminator: int, loop_behavior: LoopBehavior, src: float, target: SamplingConfig, resample: DynSincInterpolator) -> ResultModulation:
        return self.dll.AUTDModulationAudioFileCsvWithResample(path, deliminator, loop_behavior, src, target, resample)
