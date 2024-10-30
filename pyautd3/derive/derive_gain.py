from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap


def gain(cls):
    def with_cache(self):
        from pyautd3.gain.cache import Cache

        return Cache(self)

    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None):
        from pyautd3.driver.datagram.with_segment import DatagramWithSegment

        return DatagramWithSegment(self, segment, transition_mode)

    cls.with_cache = with_cache  # type: ignore[attr-defined]
    cls.with_segment = with_segment  # type: ignore[attr-defined]

    return cls
