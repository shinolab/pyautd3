from datetime import timedelta


def datagram(cls):
    def with_timeout(self, timeout: timedelta | None):
        from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout

        return DatagramWithTimeout(self, timeout)

    def with_parallel_threshold(self, threshold: int | None):
        from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

        return DatagramWithParallelThreshold(self, threshold)

    cls.with_timeout = with_timeout  # type: ignore[attr-defined]
    cls.with_parallel_threshold = with_parallel_threshold  # type: ignore[attr-defined]

    return cls
