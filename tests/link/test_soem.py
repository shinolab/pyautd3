from datetime import timedelta

import pytest

from pyautd3.link.soem import SOEM, ProcessPriority, RemoteSOEM, Status, SyncMode, ThreadPriority, TimerStrategy
from pyautd3.native_methods.autd3capi_link_soem import NativeMethods as NativeSOEM
from pyautd3.native_methods.autd3capi_link_soem import Status as _Status


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


@pytest.mark.soem
def test_status():
    lost = Status.Lost()
    state_change = Status.StateChanged()
    err = Status.Error()

    assert lost == Status.Lost()
    assert state_change == Status.StateChanged()
    assert err == Status.Error()
    assert lost != state_change
    assert lost != err
    assert lost != _Status.Lost
    assert state_change != err
    assert state_change != lost
    assert state_change != _Status.StateChanged
    assert err != lost
    assert err != state_change
    assert err != _Status.Error

    status = Status.__private_new__(_Status.Lost, "lost")
    assert status == Status.Lost()
    assert str(status) == "lost"

    with pytest.raises(NotImplementedError):
        _ = Status()


@pytest.mark.soem
def test_soem_is_default():
    builder = SOEM.builder()
    assert NativeSOEM().link_soem_is_default(
        builder.buf_size,
        int(builder.send_cycle.total_seconds() * 1000 * 1000 * 1000),
        int(builder.sync0_cycle.total_seconds() * 1000 * 1000 * 1000),
        builder.sync_mode,
        builder.process_priority,
        builder.thread_priority,
        int(builder.state_check_interval.total_seconds() * 1000 * 1000 * 1000),
        builder.timer_strategy,
        int(builder.sync_tolerance.total_seconds() * 1000 * 1000 * 1000),
        int(builder.sync_timeout.total_seconds() * 1000 * 1000 * 1000),
    )


@pytest.mark.soem
def test_soem():
    def err_handler(slave: int, status: Status) -> None:
        print(f"slave: {slave}, status: {status}")

    builder = (
        SOEM.builder()
        .with_ifname("ifname")
        .with_buf_size(10)
        .with_send_cycle(timedelta(milliseconds=10))
        .with_sync0_cycle(timedelta(milliseconds=20))
        .with_err_handler(err_handler)
        .with_timer_strategy(TimerStrategy.StdSleep)
        .with_sync_mode(SyncMode.FreeRun)
        .with_sync_tolerance(timedelta(microseconds=10))
        .with_sync_timeout(timedelta(seconds=20))
        .with_state_check_interval(timedelta(milliseconds=200))
        .with_process_priority(ProcessPriority.Idle)
        .with_thread_priority(ThreadPriority.Min)
    )
    assert builder.ifname == "ifname"
    assert builder.buf_size == 10
    assert builder.send_cycle == timedelta(milliseconds=10)
    assert builder.sync0_cycle == timedelta(milliseconds=20)
    assert builder.err_handler == err_handler
    assert builder.timer_strategy == TimerStrategy.StdSleep
    assert builder.sync_mode == SyncMode.FreeRun
    assert builder.sync_tolerance == timedelta(microseconds=10)
    assert builder.sync_timeout == timedelta(seconds=20)
    assert builder.state_check_interval == timedelta(milliseconds=200)
    assert builder.process_priority == ProcessPriority.Idle
    assert builder.thread_priority == ThreadPriority.Min


@pytest.mark.soem
def test_remote_soem():
    _ = RemoteSOEM.builder("127.0.0.1:8080")
