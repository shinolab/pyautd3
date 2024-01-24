import ctypes

from pyautd3.autd_error import AUTDError
from .autd3capi_def import AUTD3_ERR, ResultI32, ResultSamplingConfig, SamplingConfiguration
from .autd3capi_def import NativeMethods as Def


def _validate_int(res: ResultI32) -> int:
    if int(res.result) == AUTD3_ERR:
        err = ctypes.create_string_buffer(int(res.err_len))
        Def().get_err(res.err, err)
        raise AUTDError(err)
    return int(res.result)


def _validate_sampling_config(res: ResultSamplingConfig) -> SamplingConfiguration:
    if int(res.result.div) == 0:
        err = ctypes.create_string_buffer(int(res.err_len))
        Def().get_err(res.err, err)
        raise AUTDError(err)
    return res.result


def _validate_ptr(res):  # noqa: ANN001, ANN202
    if res.result._0 is None:
        err = ctypes.create_string_buffer(int(res.err_len))
        Def().get_err(res.err, err)
        raise AUTDError(err)
    return res.result
