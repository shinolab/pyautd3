from datetime import timedelta


from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap


def gain(cls):
    def with_cache(self):
        from pyautd3.gain.cache import Cache

        return Cache(self)

    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None):
        from pyautd3.driver.datagram.with_segment import DatagramWithSegment

        return DatagramWithSegment(self, segment, transition_mode)

    def with_timeout(self, timeout: timedelta | None):
        from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout

        return DatagramWithTimeout(self, timeout)

    def with_parallel_threshold(self, threshold: int | None):
        from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

        return DatagramWithParallelThreshold(self, threshold)

    cls.with_cache = with_cache  # type: ignore[attr-defined]
    cls.with_segment = with_segment  # type: ignore[attr-defined]
    cls.with_timeout = with_timeout  # type: ignore[attr-defined]
    cls.with_parallel_threshold = with_parallel_threshold  # type: ignore[attr-defined]

    return cls
