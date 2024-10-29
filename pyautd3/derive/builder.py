# type: ignore

from typing import get_type_hints
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase


def builder(cls):
    class BuilderWrap(cls):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            annotations = get_type_hints(cls)

            for attr, ty in annotations.items():
                if attr.startswith("_param_"):
                    if ty == EmitIntensity:
                        prop_name = attr[7:]
                        setter_name = f"with_{prop_name}"
                        if not hasattr(self.__class__, setter_name):

                            def setter(self, value, attr=attr):
                                from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity

                                value = EmitIntensity(value)
                                setattr(self, attr, value)
                                return self

                            setattr(self.__class__, setter_name, setter)
                    elif ty == Phase:
                        prop_name = attr[7:]
                        setter_name = f"with_{prop_name}"
                        if not hasattr(self.__class__, setter_name):

                            def setter(self, value, attr=attr):
                                from pyautd3.driver.firmware.fpga.phase import Phase

                                value = Phase(value)
                                setattr(self, attr, value)
                                return self

                            setattr(self.__class__, setter_name, setter)
                    elif attr.endswith("_u8"):
                        prop_name = attr[7:-3]
                        setter_name = f"with_{prop_name}"
                        if not hasattr(self.__class__, setter_name):

                            def setter(self, value, attr=attr):
                                from pyautd3.driver.utils import _validate_u8

                                value = _validate_u8(value)
                                setattr(self, attr, value)
                                return self

                            setattr(self.__class__, setter_name, setter)
                    else:
                        prop_name = attr[7:]
                        setter_name = f"with_{prop_name}"
                        if not hasattr(self.__class__, setter_name):

                            def setter(self, value, attr=attr):
                                setattr(self, attr, value)
                                return self

                            setattr(self.__class__, setter_name, setter)

                    if not hasattr(self.__class__, prop_name):

                        def getter(self, attr=attr):
                            return getattr(self, attr)

                        prop = property(getter)
                        setattr(self.__class__, prop_name, prop)

                if attr.startswith("_prop_"):
                    prop_name = attr[6:]
                    if not hasattr(self.__class__, prop_name):

                        def getter(self, attr=attr):
                            return getattr(self, attr)

                        prop = property(getter)
                        setattr(self.__class__, prop_name, prop)

    return BuilderWrap
