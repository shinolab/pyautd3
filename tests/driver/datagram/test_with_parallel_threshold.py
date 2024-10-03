from pyautd3.controller.controller import Controller
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.gain import Null
from pyautd3.link.audit import Audit
from pyautd3.modulation.static import Static


def test_with_parallel_threshold():
    autd: Controller[Audit]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])]).with_parallel_threshold(0).open(Audit.builder()) as autd:
        assert autd.link.last_parallel_threshold() == 0xFFFFFFFFFFFFFFFF

        autd.send(Null())
        assert autd.link.last_parallel_threshold() == 0

        autd.send(Static())
        assert autd.link.last_parallel_threshold() == 0xFFFFFFFFFFFFFFFF

        autd.send(Static().with_parallel_threshold(10))
        assert autd.link.last_parallel_threshold() == 10

        autd.send((Static(), Static()).with_parallel_threshold(5))  # type: ignore[attr-defined]
        assert autd.link.last_parallel_threshold() == 5
