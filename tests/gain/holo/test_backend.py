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
