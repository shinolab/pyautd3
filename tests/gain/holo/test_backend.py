from pyautd3.gain.holo import NalgebraBackend


def test_nalgebra_backend():
    backend = NalgebraBackend()
    backend.__del__()
    backend.__del__()
