import ctypes

from pyautd3.autd_error import AUTDError
from .autd3capi_driver import AUTD3_ERR, ResultSamplingConfig, ResultI32
from .structs import SamplingConfig
from .autd3capi import NativeMethods as Base


def _validate_int(res: ResultI32) -> int:
    if int(res.result) == AUTD3_ERR:
        err = ctypes.create_string_buffer(int(res.err_len))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return int(res.result)


def _validate_sampling_config(res: ResultSamplingConfig) -> SamplingConfig:
    if int(res.err_len) != 0:
        err = ctypes.create_string_buffer(int(res.err_len))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


def _validate_ptr(res):  # noqa: ANN001, ANN202
    if res.result._0 is None:
        err = ctypes.create_string_buffer(int(res.err_len))
        Base().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


class ConstantADT(type):
    _initialized = False

    def __setattr__(cls, name, value):
        if cls._initialized:                                            # pragma: no cover
            if name in cls.__dict__:                                    # pragma: no cover
                raise ValueError(f"Do not assign value to {name}")      # pragma: no cover
            else:                                                       # pragma: no cover
                raise AttributeError("Do not add new member to {cls}")  # pragma: no cover
        super().__setattr__(name, value)

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._initialized = True
