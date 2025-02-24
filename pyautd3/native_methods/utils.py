from pyautd3.autd_error import AUTDError
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SamplingConfigWrap
from pyautd3.native_methods.autd3capi_driver import AUTDStatus, Duration, ResultDuration, ResultF32, ResultSamplingConfig, ResultStatus, ResultU16


def _to_null_terminated_utf8(s: str) -> bytes:
    return s.encode("utf-8") + b"\0"


def _validate_status(res: ResultStatus) -> int:
    if int(res.result) == AUTDStatus.AUTDErr:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return int(res.result)


def _validate_sampling_config(res: ResultSamplingConfig) -> SamplingConfigWrap:
    if int(res.err_len) != 0:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


def _validate_duration(res: ResultDuration) -> Duration:
    if int(res.err_len) != 0:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


def _validate_u16(res: ResultU16) -> int:
    if int(res.err_len) != 0:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return int(res.result)


def _validate_f32(res: ResultF32) -> float:
    if int(res.err_len) != 0:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return float(res.result)


def _validate_ptr(res):
    if res.result.value is None:
        err = bytes(bytearray(int(res.err_len)))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


class ConstantADT(type):
    _initialized = False

    def __setattr__(cls, name, value) -> None:
        if cls._initialized:  # pragma: no cover
            if name in cls.__dict__:  # pragma: no cover
                err = f"Do not assign value to {name}"
                raise ValueError(err)  # pragma: no cover
            err = f"Do not add new member to {cls}"
            raise AttributeError(err)  # pragma: no cover
        super().__setattr__(name, value)

    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        cls._initialized = True
