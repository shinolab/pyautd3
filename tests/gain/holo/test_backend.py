"""
File: test_backend.py
Project: holo
Created Date: 04/12/2023
Author: Shun Suzuki
-----
Last Modified: 11/12/2023
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""


import pytest

from pyautd3.gain.holo import NalgebraBackend


def test_nalgebra_backend():
    backend = NalgebraBackend()
    backend.__del__()
    backend.__del__()


@pytest.mark.cuda()
def test_cuda_backend():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    backend = CUDABackend()
    backend.__del__()
    backend.__del__()
