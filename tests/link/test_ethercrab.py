import pytest

from pyautd3.link.ethercrab import CoreId, EtherCrab, EtherCrabOption, Status, ThreadPriority, tracing_init
from pyautd3.native_methods.autd3capi_link_ethercrab import NativeMethods as NativeEtherCrab
from pyautd3.native_methods.autd3capi_link_ethercrab import Status as Status_


def test_tracing_init():
    tracing_init()


def test_ethercrab_thread_priority():
    _ = ThreadPriority.Max
    _ = ThreadPriority.Min
    _ = ThreadPriority.Crossplatform(0)
    _ = ThreadPriority.Crossplatform(99)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(-1)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(100)


def test_status():
    lost = Status.Lost()
    state_change = Status.StateChanged()
    err = Status.Error()

    assert lost == Status.Lost()
    assert state_change == Status.StateChanged()
    assert err == Status.Error()
    assert lost != state_change
    assert lost != err
    assert lost != Status_.Lost
    assert state_change != err
    assert state_change != lost
    assert state_change != Status_.StateChanged
    assert err != lost
    assert err != state_change
    assert err != Status_.Error

    status = Status.__private_new__(Status_.Lost, "lost")
    assert status == Status.Lost()
    assert str(status) == "lost"

    with pytest.raises(NotImplementedError):
        _ = Status()


def test_ethercrab_is_default():
    assert NativeEtherCrab().link_ether_crab_is_default(EtherCrabOption()._inner())


def test_ethercrab():
    def err_handler(slave: int, status: Status) -> None:
        print(f"slave: {slave}, status: {status}")

    _ = EtherCrab(err_handler, EtherCrabOption(main_thread_affinity=CoreId(0)))
