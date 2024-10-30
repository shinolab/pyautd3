def gain(cls):
    def with_cache(self):
        from pyautd3.gain.cache import Cache

        return Cache(self)

    cls.with_cache = with_cache  # type: ignore[attr-defined]

    return cls
