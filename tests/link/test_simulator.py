from pyautd3.link.simulator import Simulator


def test_simulator():
    _ = Simulator.builder("127.0.0.1:8080")
