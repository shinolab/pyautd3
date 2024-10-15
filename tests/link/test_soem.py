from datetime import timedelta

import pytest

from pyautd3 import AUTD3, Controller
from pyautd3.autd_error import AUTDError
from pyautd3.link.soem import SOEM, ProcessPriority, RemoteSOEM, Status, SyncMode, ThreadPriority, TimerStrategy


@pytest.mark.soem
def test_soem_adapers():
    adapters = SOEM.enumerate_adapters()
    for adapter in adapters:
        print(adapter)


@pytest.mark.soem
def test_soem_thread_priority():
    _ = ThreadPriority.Max
    _ = ThreadPriority.Min
    _ = ThreadPriority.Crossplatform(0)
    _ = ThreadPriority.Crossplatform(99)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(-1)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(100)


def err_handler(slave: int, status: Status, msg: str) -> None:
    print(f"slave: {slave}, status: {status}, msg: {msg}")


@pytest.mark.soem
def test_soem():
    with (
        pytest.raises(AUTDError) as _,
        (
            Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
                SOEM.builder()
                .with_ifname("")
                .with_buf_size(32)
                .with_send_cycle(2)
                .with_sync0_cycle(2)
                .with_err_handler(err_handler)
                .with_timer_strategy(TimerStrategy.Sleep)
                .with_sync_mode(SyncMode.DC)
                .with_sync_tolerance(timedelta(microseconds=1))
                .with_sync_timeout(timedelta(seconds=10))
                .with_state_check_interval(timedelta(milliseconds=100))
                .with_process_priority(ProcessPriority.High)
                .with_thread_priority(ThreadPriority.Max)
                .with_timeout(timedelta(milliseconds=200)),
            )
        ) as _,
    ):
        pass


@pytest.mark.soem
def test_remote_soem():
    _ = RemoteSOEM.builder("127.0.0.1:8080").with_timeout(timedelta(milliseconds=200))
