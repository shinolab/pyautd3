from pyautd3.controller.controller import Controller
from pyautd3.driver.autd3_device import AUTD3
from pyautd3.gain import Null
from pyautd3.link.audit import Audit
from pyautd3.modulation.static import Static


def test_with_parallel_threshold():
    autd: Controller[Audit]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        autd.send(Static().with_parallel_threshold(None))
        assert autd.link.last_parallel_threshold() is None

        autd.send(Static().with_parallel_threshold(10))
        assert autd.link.last_parallel_threshold() == 10

        autd.send((Null(), Static()).with_parallel_threshold(20))  # type: ignore[attr-defined]
        assert autd.link.last_parallel_threshold() == 20
